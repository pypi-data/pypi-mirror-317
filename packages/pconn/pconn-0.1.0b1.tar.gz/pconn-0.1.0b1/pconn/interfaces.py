"""The methods for loading Gallagher plugins interfaces."""

from __future__ import annotations

import asyncio
from collections.abc import Iterable
from functools import cached_property
import importlib.util
import logging
import pathlib
from types import ModuleType
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypedDict, cast

from awesomeversion import AwesomeVersion

from . import generated
from .core import PConn
from .util.json import JSON_DECODE_EXCEPTIONS, json_loads

if TYPE_CHECKING:
    from .plugin_entries import PluginEntry

_LOGGER = logging.getLogger(__name__)

DATA_COMPONENTS = "components"
DATA_INTERFACES = "interfaces"


class Manifest(TypedDict, total=False):
    """Interface manifest."""

    name: str
    domain: str
    dependencies: list[str]
    requirements: list[str]
    documentation: str
    version: str
    interface_type: Literal["platform", "plugin"]


class Interface:
    """An interface in Gallagher Plugins."""

    @classmethod
    def resolve_from_root(
        cls, pconn: PConn, root_module: ModuleType, domain: str
    ) -> Interface | None:
        """Resolve an integration from a root module."""
        for base in root_module.__path__:
            manifest_path = pathlib.Path(base) / domain / "manifest.json"

            if not manifest_path.is_file():
                continue

            try:
                manifest = cast(Manifest, json_loads(manifest_path.read_text()))
            except JSON_DECODE_EXCEPTIONS as err:
                _LOGGER.error(
                    "Error parsing manifest.json file at %s: %s", manifest_path, err
                )
                continue

            integration = cls(
                pconn,
                f"{root_module.__name__}.{domain}",
                manifest_path.parent,
                manifest,
            )
            return integration

        return None

    def __init__(
        self,
        pconn: PConn,
        pkg_path: str,
        file_path: pathlib.Path,
        manifest: Manifest,
    ) -> None:
        """Initialize an interface."""
        self.pconn = pconn
        self.pkg_path = pkg_path
        self.file_path = file_path
        self.manifest = manifest
        if self.dependencies:
            self._all_dependencies_resolved: bool | None = None
            self._all_dependencies: set[str] | None = None
        else:
            self._all_dependencies_resolved = True
            self._all_dependencies = set()

        _LOGGER.info("Loaded %s from %s", self.domain, pkg_path)

    @cached_property
    def name(self) -> str:
        """Return name."""
        return self.manifest["name"]

    @cached_property
    def domain(self) -> str:
        """Return domain."""
        return self.manifest["domain"]

    @cached_property
    def dependencies(self) -> list[str]:
        """Return dependencies."""
        return self.manifest.get("dependencies", [])

    @cached_property
    def requirements(self) -> list[str]:
        """Return requirements."""
        return self.manifest.get("requirements", [])

    @cached_property
    def documentation(self) -> str | None:
        """Return documentation."""
        return self.manifest.get("documentation")

    @cached_property
    def interface_type(
        self,
    ) -> Literal["platform", "plugin"]:
        """Return the interface type."""
        return self.manifest.get("interface_type", "plugin")

    @cached_property
    def version(self) -> AwesomeVersion:
        """Return the version of the integration."""
        return AwesomeVersion(self.manifest["version"])

    @property
    def all_dependencies(self) -> set[str]:
        """Return all dependencies including sub-dependencies."""
        if self._all_dependencies is None:
            raise RuntimeError("Dependencies not resolved!")

        return self._all_dependencies

    @property
    def all_dependencies_resolved(self) -> bool:
        """Return if all dependencies have been resolved."""
        return self._all_dependencies_resolved is not None

    async def resolve_dependencies(self) -> bool:
        """Resolve all dependencies."""
        if self._all_dependencies_resolved is not None:
            return self._all_dependencies_resolved

        self._all_dependencies_resolved = False
        try:
            dependencies = await _async_component_dependencies(self.pconn, self)
        except InterfaceNotFound as err:
            _LOGGER.error(
                (
                    "Unable to resolve dependencies for %s:  we are unable to resolve"
                    " (sub)dependency %s"
                ),
                self.domain,
                err.domain,
            )
        except CircularDependency as err:
            _LOGGER.error(
                (
                    "Unable to resolve dependencies for %s:  it contains a circular"
                    " dependency: %s -> %s"
                ),
                self.domain,
                err.from_domain,
                err.to_domain,
            )
        else:
            dependencies.discard(self.domain)
            self._all_dependencies = dependencies
            self._all_dependencies_resolved = True

        return self._all_dependencies_resolved

    def get_component(self) -> ComponentProtocol:
        """Return the component."""
        cache: dict[str, ComponentProtocol] = self.pconn.data[DATA_COMPONENTS]
        if self.domain in cache:
            return cache[self.domain]

        try:
            cache[self.domain] = cast(
                ComponentProtocol, importlib.import_module(self.pkg_path)
            )
        except ImportError:
            raise
        except Exception as err:
            _LOGGER.exception(
                "Unexpected exception importing component %s", self.pkg_path
            )
            raise ImportError(f"Exception importing {self.pkg_path}") from err

        return cache[self.domain]

    def get_platform(self, platform_name: str) -> ModuleType:
        """Return a platform for an integration."""
        cache: dict[str, ModuleType] = self.pconn.data[DATA_COMPONENTS]
        full_name = f"{self.domain}.{platform_name}"
        if full_name in cache:
            return cache[full_name]

        try:
            cache[full_name] = self._import_platform(platform_name)
        except ImportError:
            raise
        except Exception as err:
            _LOGGER.exception(
                "Unexpected exception importing platform %s.%s",
                self.pkg_path,
                platform_name,
            )
            raise ImportError(
                f"Exception importing {self.pkg_path}.{platform_name}"
            ) from err

        return cache[full_name]

    def _import_platform(self, platform_name: str) -> ModuleType:
        """Import the platform."""
        return importlib.import_module(f"{self.pkg_path}.{platform_name}")

    def __repr__(self) -> str:
        """Text representation of class."""
        return f"<Interface {self.domain}: {self.pkg_path}>"


class ComponentProtocol(Protocol):
    """Define the format of an interface."""

    DOMAIN: str

    async def async_setup(self, hass: PConn) -> bool:
        """Set up interface."""

    async def async_setup_entry(self, hass: PConn, config_entry: PluginEntry) -> bool:
        """Set up a config entry."""

    async def async_unload_entry(self, hass: PConn, config_entry: PluginEntry) -> bool:
        """Unload a config entry."""


async def async_setup(pconn: PConn) -> None:
    """Setup necessary data structures."""
    pconn.data[DATA_COMPONENTS] = {}
    pconn.data[DATA_INTERFACES] = {}


def get_interface_descriptions(
    pconn: PConn,
) -> dict[str, Any]:
    """Return interfaces description."""
    base = generated.__path__[0]
    interfaces_path = pathlib.Path(base) / "interfaces.json"

    data = interfaces_path.read_text()
    interfaces = cast(dict[str, Any], json_loads(data))
    return {
        "plugins": {
            key: value
            for key, value in interfaces.items()
            if value["interface_type"] == "plugin"
        },
        "licensedPlugins": list(pconn.lic_file.licensed_plugins()),
    }


async def async_get_interface(pconn: PConn, domain: str) -> Interface:
    """Get interface."""
    interfaces_or_excs = await async_get_interfaces(pconn, [domain])
    int_or_exc = interfaces_or_excs[domain]
    if isinstance(int_or_exc, Interface):
        return int_or_exc
    raise int_or_exc


async def async_get_interfaces(  # noqa: C901
    pconn: PConn, domains: Iterable[str]
) -> dict[str, Interface | Exception]:
    """Get interface."""
    cache = pconn.data[DATA_INTERFACES]
    results: dict[str, Interface | Exception] = {}
    needed: dict[str, asyncio.Future[None]] = {}
    in_progress: dict[str, asyncio.Future[None]] = {}

    if TYPE_CHECKING:
        cache = cast(dict[str, Interface | asyncio.Future[None]], cache)

    for domain in domains:
        int_or_fut = cache.get(domain, None)
        # Interface is never subclassed, so we can check for type
        if type(int_or_fut) is Interface:  # noqa: E721
            results[domain] = int_or_fut
        elif int_or_fut is not None:
            in_progress[domain] = cast(asyncio.Future[None], int_or_fut)
        elif "." in domain:
            results[domain] = ValueError(f"Invalid domain {domain}")
        else:
            needed[domain] = cache[domain] = pconn.loop.create_future()

    if in_progress:
        await asyncio.gather(*in_progress.values())
        for domain in in_progress:
            # When we have waited and it's _UNDEF, it doesn't exist
            # We don't cache that it doesn't exist, or else people can't fix it
            # and then restart, because their config will never be valid.
            if (int_or_fut := cache.get(domain, None)) is None:
                results[domain] = InterfaceNotFound(domain)
            else:
                results[domain] = cast(Interface, int_or_fut)

    if not needed:
        return results

    from . import plugins  # pylint: disable=import-outside-toplevel

    interfaces = await pconn.async_add_executor_job(
        _resolve_integrations_from_root, pconn, plugins, list(needed)
    )

    for domain, future in needed.items():
        int_or_exc = interfaces.get(domain)
        if not int_or_exc:
            cache.pop(domain)
            results[domain] = InterfaceNotFound(domain)
        elif isinstance(int_or_exc, Exception):
            cache.pop(domain)
            exc = InterfaceNotFound(domain)
            exc.__cause__ = int_or_exc
            results[domain] = exc
        else:
            results[domain] = cache[domain] = int_or_exc
        future.set_result(None)

    return results


def _resolve_integrations_from_root(
    pconn: PConn, root_module: ModuleType, domains: list[str]
) -> dict[str, Interface]:
    """Resolve multiple integrations from root."""
    interfaces: dict[str, Interface] = {}
    for domain in domains:
        try:
            interface = Interface.resolve_from_root(pconn, root_module, domain)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Error loading integration: %s", domain)
        else:
            if interface:
                interfaces[domain] = interface
    return interfaces


async def _async_component_dependencies(
    pconn: PConn,
    interface: Interface,
) -> set[str]:
    """Get component dependencies."""
    loading: set[str] = set()
    loaded: set[str] = set()

    async def component_dependencies_impl(interface: Interface) -> None:
        """Recursively get component dependencies."""
        domain = interface.domain
        if not (dependencies := interface.dependencies):
            loaded.add(domain)
            return

        loading.add(domain)
        dep_integrations = await async_get_interfaces(pconn, dependencies)
        for dependency_domain, dep_integration in dep_integrations.items():
            if isinstance(dep_integration, Exception):
                raise dep_integration

            # If we have already loaded it, no point doing it again.
            if dependency_domain in loaded:
                continue

            # If we are already loading it, we have a circular dependency.
            if dependency_domain in loading:
                raise CircularDependency(dependency_domain, domain)

            await component_dependencies_impl(dep_integration)
        loading.remove(domain)
        loaded.add(domain)

    await component_dependencies_impl(interface)

    return loaded


class LoaderError(Exception):
    """Loader base error."""


class InterfaceNotFound(LoaderError):
    """Raised when a plugin is not found."""

    def __init__(self, domain: str) -> None:
        """Initialize a plugin not found error."""
        super().__init__(f"Interface '{domain}' not found.")
        self.domain = domain


class CircularDependency(LoaderError):
    """Raised when a circular dependency is found when resolving components."""

    def __init__(self, from_domain: str | set[str], to_domain: str) -> None:
        """Initialize circular dependency error."""
        super().__init__(f"Circular dependency detected: {from_domain} -> {to_domain}.")
        self.from_domain = from_domain
        self.to_domain = to_domain
