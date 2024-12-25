"""Helper to validate the license file."""

from __future__ import annotations

import base64
from dataclasses import dataclass
import json
import logging
import pathlib
import shutil
from typing import TYPE_CHECKING, Any, NotRequired, Required, TypedDict, cast

from pyasn1.error import PyAsn1Error
import rsa

if TYPE_CHECKING:
    from pconn.core import PConn
from pconn.const import __short_version__, __version__

DOMAIN = "license_handler"
LICENSE_KEY = ".license"

_LOGGER = logging.getLogger(__name__)


class LicenseError(Exception):
    """Base exception for license errors."""


class LicenseNotValid(LicenseError):
    """Raise exception if license is not valid."""


class LicenseNotFound(LicenseError):
    """Raise exception if license is not found."""


class PluginInfo(TypedDict, total=False):
    """Plugin info dictionary."""

    name: Required[str]
    token: str
    limit: int


class LicenseInfo(TypedDict):
    """License information dictionary."""

    serial_number: int
    version: str
    workstations: int
    plugins: list[PluginInfo]
    validation_token: NotRequired[str]


@dataclass
class LicenseFile:
    """Class representing a license file."""

    license: LicenseInfo
    validation: str
    public_key: str
    valid: bool = False

    @property
    def serial_number(self) -> int:
        """Return the serial number."""
        return self.license["serial_number"]

    @property
    def version(self) -> str:
        """Return the license version."""
        return self.license["version"]

    @property
    def workstations(self) -> int:
        """Return the workstations limit."""
        return self.license["workstations"]

    def as_dict(self) -> dict[str, Any]:
        """Return license as dictionary."""
        return {
            "serial_number": self.serial_number,
            "version": __version__,
            "plugins": list(self.licensed_plugins()),
            "licensed_workstations": self.workstations,
        }

    def licensed_plugins(self) -> dict[str, PluginInfo]:
        """Return list of licensed plugins."""
        if not self.valid:
            return {}
        return {plugin["name"]: plugin for plugin in self.license["plugins"]}

    def get_token(self, key: str) -> str | None:
        """Return token to be used."""
        if key == "core":
            return self.license.get("validation_token")
        if plugin := self.licensed_plugins().get(key):
            return plugin.get("token")
        return None

    @classmethod
    def load_license(cls, file_path: pathlib.Path) -> LicenseFile:
        """Create a LicenseFile instance from the file."""
        if not file_path.exists():
            raise LicenseNotFound("License file is not found")
        try:
            lic_content = cast(dict[str, Any], json.loads(file_path.read_text()))
        except json.JSONDecodeError as err:
            raise LicenseNotValid("License file is not valid") from err
        lic_details = json.loads(base64.b64decode(lic_content["license"]).decode())
        public_key = base64.b64decode(lic_content["public_key"]).decode()
        return LicenseFile(
            license=lic_details,
            validation=lic_content["validation"],
            public_key=public_key,
        )

    @classmethod
    def delete_license(cls, file_path: pathlib.Path) -> None:
        """Delete license file."""
        if not file_path.exists():
            return
        file_path.unlink()

    def verify_license(self) -> None:
        """Verify that the license is authentic."""
        try:
            public_key = rsa.PublicKey.load_pkcs1(self.public_key.encode())
            rsa.verify(
                json.dumps(self.license).encode(),
                bytes.fromhex(self.validation),
                public_key,
            )
            _LOGGER.info("License file is valid.")
        except (PyAsn1Error, rsa.VerificationError) as err:
            self.valid = False
            message = "License file invalid."
            raise LicenseNotValid(message) from err
        if self.license["version"] != __short_version__:
            raise LicenseNotValid("License version does not match.")
        self.valid = True


def validate_uploaded_license(pconn: PConn, file_id: str) -> None:
    """Validate new license file."""
    # pylint: disable=import-outside-toplevel
    from pconn.helpers.file_upload import process_uploaded_file

    with process_uploaded_file(pconn, file_id) as file_path:
        validate_license(pconn, file_path)
        shutil.move(file_path, pconn.config.path(LICENSE_KEY))


def validate_license(pconn: PConn, path: pathlib.Path) -> None:
    """Validate the license file."""
    lic_file = LicenseFile.load_license(path)
    try:
        lic_file.verify_license()
    except Exception as err:  # pylint: disable=broad-except
        raise LicenseNotValid(str(err)) from err
    if pconn.lic_file:
        if pconn.lic_file.serial_number != lic_file.serial_number:
            raise LicenseNotValid("Invalid serial number in license file.")
        if len(pconn.workstations.registered_workstations) > lic_file.workstations:
            raise LicenseNotValid("Configured workstations exceed license limit.")
        licensed_plugins = list(lic_file.licensed_plugins())
        for domain in pconn.plugin_entries.async_domains():
            if domain not in licensed_plugins:
                raise LicenseNotValid(f"Plugin '{domain}' is not licensed.")
    pconn.lic_file = lic_file


def delete_license(pconn: PConn) -> None:
    """Delete license file."""
    LicenseFile.delete_license(pathlib.Path(pconn.config.path(LICENSE_KEY)))
    pconn.lic_file = None  # type: ignore[assignment]
