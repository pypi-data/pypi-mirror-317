"""Module to handle installing requirements."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from .core import PConn
from .exceptions import PConnError
from .interfaces import Interface
from .util import package as pkg_util

_LOGGER = logging.getLogger(__name__)

PIP_TIMEOUT = 60
MAX_INSTALL_FAILURES = 3
DATA_REQUIREMENTS_MANAGER = "requirements_manager"


class RequirementsNotFound(PConnError):
    """Raised when a component is not found."""

    def __init__(self, domain: str, requirements: list[str]) -> None:
        """Initialize a component not found error."""
        super().__init__(f"Requirements for {domain} not found: {requirements}.")
        self.domain = domain
        self.requirements = requirements


async def async_process_requirements(
    pconn: PConn, name: str, requirements: list[str]
) -> None:
    """Install the requirements for a component or platform.

    This method is a coroutine. It will raise RequirementsNotFound
    if an requirement can't be satisfied.
    """
    await _async_get_manager(pconn).async_process_requirements(name, requirements)


def _async_get_manager(pconn: PConn) -> RequirementsManager:
    """Get the requirements manager."""
    manager: RequirementsManager | None = pconn.data.get(DATA_REQUIREMENTS_MANAGER)
    if manager is None:
        manager = pconn.data[DATA_REQUIREMENTS_MANAGER] = RequirementsManager(pconn)
    return manager


def _install_with_retry(requirement: str, kwargs: dict[str, Any]) -> bool:
    """Try to install a package up to MAX_INSTALL_FAILURES times."""
    for _ in range(MAX_INSTALL_FAILURES):
        if pkg_util.install_package(requirement, **kwargs):
            return True
    return False


def _install_requirements_if_missing(
    requirements: list[str], kwargs: dict[str, Any]
) -> tuple[set[str], set[str]]:
    """Install requirements if missing."""
    installed: set[str] = set()
    failures: set[str] = set()
    for req in requirements:
        if pkg_util.is_installed(req) or _install_with_retry(req, kwargs):
            installed.add(req)
            continue
        failures.add(req)
    return installed, failures


class RequirementsManager:
    """Manage requirements."""

    def __init__(self, pconn: PConn) -> None:
        """Init the requirements manager."""
        self.pconn = pconn
        self.pip_lock = asyncio.Lock()
        self.interfaces_with_reqs: dict[
            str, Interface | asyncio.Future[None] | None
        ] = {}
        self.install_failure_history: set[str] = set()
        self.is_installed_cache: set[str] = set()

    async def async_process_requirements(
        self, name: str, requirements: list[str]
    ) -> None:
        """Install the requirements for a interface.

        This method is a coroutine. It will raise RequirementsNotFound
        if an requirement can't be satisfied.
        """
        if not (missing := self._find_missing_requirements(requirements)):
            return
        self._raise_for_failed_requirements(name, missing)

        async with self.pip_lock:
            # Recalculate missing again now that we have the lock
            if missing := self._find_missing_requirements(requirements):
                await self._async_process_requirements(name, missing)

    def _find_missing_requirements(self, requirements: list[str]) -> list[str]:
        """Find requirements that are missing in the cache."""
        return [req for req in requirements if req not in self.is_installed_cache]

    def _raise_for_failed_requirements(
        self, interface: str, missing: list[str]
    ) -> None:
        """Raise for failed installing interface requirements.

        Raise RequirementsNotFound so we do not keep trying requirements
        that have already failed.
        """
        for req in missing:
            if req in self.install_failure_history:
                _LOGGER.info(
                    (
                        "Multiple attempts to install %s failed, install will be"
                        " retried after next configuration check or restart"
                    ),
                    req,
                )
                raise RequirementsNotFound(interface, [req])

    async def _async_process_requirements(
        self,
        name: str,
        requirements: list[str],
    ) -> None:
        """Install a requirement and save failures."""
        kwargs = {"timeout": PIP_TIMEOUT}
        installed, failures = await self.pconn.async_add_executor_job(
            _install_requirements_if_missing, requirements, kwargs
        )
        self.is_installed_cache |= installed
        self.install_failure_history |= failures
        if failures:
            raise RequirementsNotFound(name, list(failures))
