"""Translation string lookup helpers."""
from __future__ import annotations

import asyncio
from collections.abc import Iterable, Mapping
import logging
from typing import Any

from pconn.core import PConn
from pconn.interfaces import Interface, async_get_interfaces
from pconn.util.json import load_json

_LOGGER = logging.getLogger(__name__)

TRANSLATION_LOAD_LOCK = "translation_load_lock"
TRANSLATION_FLATTEN_CACHE = "translation_flatten_cache"
LOCALE_EN = "en"


def recursive_flatten(prefix: Any, data: dict[str, Any]) -> dict[str, Any]:
    """Return a flattened representation of dict data."""
    output = {}
    for key, value in data.items():
        if isinstance(value, dict):
            output.update(recursive_flatten(f"{prefix}{key}.", value))
        else:
            output[f"{prefix}{key}"] = value
    return output


def load_translations_files(
    translation_files: dict[str, str]
) -> dict[str, dict[str, Any]]:
    """Load and parse translation.json files."""
    loaded = {}
    for component, translation_file in translation_files.items():
        loaded_json = load_json(translation_file)

        if not isinstance(loaded_json, dict):
            _LOGGER.warning(
                "Translation file is unexpected type %s. Expected dict for %s",
                type(loaded_json),
                translation_file,
            )
            continue

        loaded[component] = loaded_json

    return loaded


def _build_resources(
    translation_strings: dict[str, dict[str, Any]],
    components: set[str],
    category: str,
) -> dict[str, dict[str, Any] | str]:
    """Build the resources response for the given components."""
    # Build response
    return {
        component: translation_strings[component][category]
        for component in components
        if category in translation_strings[component]
        and translation_strings[component][category] is not None
    }


async def _async_get_component_strings(
    pconn: PConn,
    components: set[str],
    interfaces: dict[str, Interface],
) -> dict[str, Any]:
    """Load translations."""
    translations: dict[str, Any] = {}
    # Determine paths of missing components/platforms
    files_to_load = {}
    for domain in components:
        interface = interfaces[domain]

        path = interface.file_path / "strings.json"
        # No translation available
        if not path.exists():
            translations[domain] = {}
        else:
            files_to_load[domain] = path

    if not files_to_load:
        return translations

    # Load files
    load_translations_job = pconn.async_add_executor_job(
        load_translations_files, files_to_load
    )
    assert load_translations_job is not None
    loaded_translations = await load_translations_job

    # Translations that miss "title" will get integration put in.
    for domain, loaded_translation in loaded_translations.items():
        if "title" not in loaded_translation:
            loaded_translation["title"] = interfaces[domain].name

    translations.update(loaded_translations)

    return translations


class _TranslationCache:
    """Cache for flattened translations."""

    def __init__(self, pconn: PConn) -> None:
        """Initialize the cache."""
        self.pconn = pconn
        self.loaded: set[str] = set()
        self.cache: dict[str, dict[str, Any]] = {}

    async def async_fetch(
        self,
        components: set[str],
    ) -> list[dict[str, dict[str, Any]]]:
        """Load resources into the cache."""
        components_to_load = components - self.loaded

        if components_to_load:
            await self._async_load(components_to_load)

        cached = self.cache

        return [cached.get(component, {}) for component in components]

    async def _async_load(self, components: set[str]) -> None:
        """Populate the cache for a given set of components."""
        _LOGGER.debug(
            "Cache miss for %s",
            ", ".join(components),
        )

        interfaces: dict[str, Interface] = {}
        ints_or_excs = await async_get_interfaces(self.pconn, components)
        for domain, int_or_exc in ints_or_excs.items():
            if isinstance(int_or_exc, Exception):
                raise int_or_exc
            interfaces[domain] = int_or_exc

        translation_strings = await _async_get_component_strings(
            self.pconn, components, interfaces
        )
        self._build_category_cache(components, translation_strings)

        self.loaded.update(components)

    def _build_category_cache(
        self,
        components: set[str],
        translation_strings: dict[str, dict[str, Any]],
    ) -> None:
        """Extract resources into the cache."""
        resource: dict[str, Any] | str
        cached = self.cache
        categories: set[str] = set()
        for resource in translation_strings.values():
            categories.update(resource)

        for category in categories:
            new_resources: Mapping[str, dict[str, Any] | str]
            new_resources = _build_resources(translation_strings, components, category)

            for component, resource in new_resources.items():
                cached.setdefault(component, {})[category] = resource


async def async_get_translations(
    pconn: PConn,
    interfaces: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Return all backend translations.

    If interface specified, load it for that one.
    Otherwise default to loaded interfaces.
    """
    lock = pconn.data.setdefault(TRANSLATION_LOAD_LOCK, asyncio.Lock())

    if interfaces is not None:
        components = set(interfaces)
    else:
        components = pconn.config.interfaces

    async with lock:
        if TRANSLATION_FLATTEN_CACHE in pconn.data:
            cache = pconn.data[TRANSLATION_FLATTEN_CACHE]
        else:
            cache = pconn.data[TRANSLATION_FLATTEN_CACHE] = _TranslationCache(pconn)
        cached = await cache.async_fetch(components)

    result = {}
    for entry in cached:
        result.update(entry)
    return result
