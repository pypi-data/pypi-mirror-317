"""Provide methods to bootstrap a Gallagher plugin instance."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from . import interfaces, requirements
from .exceptions import DependencyError, PConnError

if TYPE_CHECKING:
    from .core import PConn

DATA_SETUP = "setup"
DATA_SETUP_DONE = "setup_done"
DATA_DEPENDENCIES = "dependencies"
DATA_DEPS_REQS = "deps_reqs"


_LOGGER = logging.getLogger(__name__)


async def async_setup_interface(pconn: PConn, domain: str) -> bool:
    """Setup an interface for Gallagher plugins."""
    if domain in pconn.config.interfaces:
        return True

    try:
        interface = await interfaces.async_get_interface(pconn, domain)
    except interfaces.InterfaceNotFound:
        _LOGGER.error("Interface %s not found.", domain)
        return False

    # Validate all dependencies exist and there are no circular dependencies
    if not await interface.resolve_dependencies():
        return False

    # Process requirements as soon as possible, so we can import the component
    # without requiring imports to be in functions.
    try:
        await async_process_deps_reqs(pconn, interface)
    except PConnError as err:
        _LOGGER.error("Error processing requirements: %s", err)
        return False

    try:
        component = interface.get_component()
    except ImportError as err:
        _LOGGER.error("Unable to import component: %s", err)
        return False

    if hasattr(component, "async_setup"):
        if not await component.async_setup(pconn):
            _LOGGER.error("Interface failed to setup")
            return False

    pconn.config.interfaces.add(domain)
    if not hasattr(component, "async_setup_entry"):
        if interface.interface_type == "platform":
            return True
        _LOGGER.error("No plugin entry setup function defined.")
        return False
    await asyncio.gather(
        *(
            asyncio.create_task(
                entry.async_setup(pconn, interface=interface),
                name=f"plugn entry setup {entry.title} {entry.domain} {entry.entry_id}",
            )
            for entry in pconn.plugin_entries.async_entries(domain)
        )
    )
    return True


async def async_process_deps_reqs(
    pconn: PConn, interface: interfaces.Interface
) -> None:
    """Process all dependencies and requirements for a module.

    Module is a Python module of either a component or platform.
    """
    if (processed := pconn.data.get(DATA_DEPS_REQS)) is None:
        processed = pconn.data[DATA_DEPS_REQS] = set()
    elif interface.domain in processed:
        return

    if failed_deps := await _async_process_dependencies(pconn, interface):
        raise DependencyError(failed_deps)

    await requirements.async_process_requirements(
        pconn, interface.name, interface.requirements
    )

    processed.add(interface.domain)


async def _async_process_dependencies(
    pconn: PConn, interface: interfaces.Interface
) -> list[str]:
    """Ensure all dependencies are set up.

    Returns a list of dependencies which failed to set up.
    """
    setup_futures = pconn.data.setdefault(DATA_SETUP, {})

    if not (
        dependencies_tasks := {
            dep: setup_futures.get(dep)
            or pconn.loop.create_task(
                async_setup_interface(pconn, dep),
                name=f"setup {dep} as dependency of {interface.domain}",
            )
            for dep in interface.dependencies
        }
    ):
        return []

    _LOGGER.debug(
        "Dependency %s will wait for dependencies %s",
        interface.domain,
        dependencies_tasks.keys(),
    )

    results = await asyncio.gather(*dependencies_tasks.values())

    failed = [
        domain for idx, domain in enumerate(dependencies_tasks) if not results[idx]
    ]

    if failed:
        _LOGGER.error(
            "Unable to set up dependencies of '%s'. Setup failed for dependencies: %s",
            interface.domain,
            failed,
        )

    return failed
