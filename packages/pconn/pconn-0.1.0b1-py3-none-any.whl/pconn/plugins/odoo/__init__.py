"""Plugin for interfacing with Odoo system."""

from __future__ import annotations

from datetime import datetime
import socket
from typing import Any, cast
from xmlrpc import client as xmlrpclib

from pconn.core import PConn
from pconn.exceptions import PluginEntryError, PluginEntryNotReady
from pconn.plugin_entries import PluginEntry

from .errors import ConfigError, ConnectError, InvalidAuth, OdooError, RequestError

DOMAIN = "odoo"


async def async_setup_entry(pconn: PConn, entry: PluginEntry[OdooClient]) -> bool:
    """Setup plugin from plugin entry."""
    odoo_client = OdooClient(**entry.data)
    try:
        await pconn.async_add_executor_job(odoo_client.connect)
    except TimeoutError as err:
        raise PluginEntryNotReady(
            "Error: Timeout reached. Check connection settings."
        ) from err
    except OdooError as err:
        raise PluginEntryError(str(err)) from err

    entry.plugin_data = odoo_client

    return True


class OdooClient:
    """Odoo client class."""

    def __init__(
        self,
        *,
        protocol: str,
        host: str,
        port: int,
        db_name: str,
        username: str,
        password: str,
    ) -> None:
        """Initiate client."""
        self.host = host
        self.db = db_name
        self.username = username
        self.password = password
        self.uid: Any = None
        self.client = xmlrpclib.ServerProxy(
            f"{protocol}://{host}:{port}/xmlrpc/2/common"
        )
        self.models = xmlrpclib.ServerProxy(
            f"{protocol}://{host}:{port}/xmlrpc/2/object"
        )
        self.connected = False
        socket.setdefaulttimeout(10)

    # TODO: add execute_kw method with exceptions and updated connected status
    def _execute_command(
        self,
        table: str,
        command: str,
        _filter: list[Any],
        params: dict[str, Any],
    ) -> Any:
        """Execute model command and return result."""
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password, table, command, _filter, params
            )
        except socket.gaierror as err:
            self.connected = False
            raise ConnectError(f"Cannot resolve hostname: {self.host}") from err
        except (ConnectionRefusedError, TimeoutError) as err:
            self.connected = False
            raise ConnectError(
                "Connection refused. Verify host and port are correct."
            ) from err
        except xmlrpclib.Fault as err:
            try:
                exception_message = err.faultString.splitlines()[-2].strip()
            except IndexError:
                exception_message = err.faultString
            if "database" in exception_message:
                exception_message = "Invalid database name"
            elif "hr.attendance doesn't exist" in exception_message:
                exception_message = "Attendance module is not installed"
            else:
                raise RequestError(exception_message)
            raise ConfigError(exception_message) from err

    def connect(self) -> None:
        """Connect to Odoo system."""
        try:
            self.uid = self.client.authenticate(
                self.db,
                self.username,
                self.password,
                {},
            )
        except socket.gaierror as err:
            raise ConnectError(f"Cannot resolve hostname: {self.host}") from err
        except (ConnectionRefusedError, TimeoutError, xmlrpclib.ProtocolError) as err:
            raise ConnectError(
                f"Error: Connection refused. Verify host and port are correct. {err}"
            ) from err
        except xmlrpclib.Fault as err:
            try:
                exception_message = err.faultString.splitlines()[-2].strip()
            except IndexError:
                exception_message = err.faultString
            if "database" in exception_message:
                exception_message = "Invalid database name"
            elif "hr.attendance doesn't exist" in exception_message:
                exception_message = "Attendance module is not installed"
            raise ConfigError(exception_message) from err
        if not self.uid:
            raise InvalidAuth("Invalid credentials")
        if not self._execute_command(
            "hr.attendance",
            "check_access_rights",
            ["create"],
            {"raise_exception": False},
        ):
            raise ConfigError("User is not allowed to create attendance")
        self.connected = True

    def get_employee_fields(self) -> dict[str, str]:
        """Return employee id for a given emp_id."""
        if result := cast(
            dict[str, Any],
            self._execute_command(
                "hr.employee", "fields_get", [], {"attributes": ["string", "type"]}
            ),
        ):
            return {
                field: info["string"]
                for field, info in result.items()
                if info["type"] == "char"
            }
        return {}

    def get_employee_id(self, field: str, value: str) -> str | None:
        """Return employee id for a given emp_id."""
        if employee_ids := self._execute_command(
            "hr.employee", "search", [[[field, "=", value]]], {}
        ):
            return cast(list[str], employee_ids)[0]
        return None

    def get_last_attendance(self, id: str) -> dict[str, Any]:
        """Return last attendance for a given employee."""
        last_attendance: dict[str, Any] = {}
        if response := self._execute_command(
            "hr.attendance",
            "search_read",
            [[["employee_id", "=", id]]],
            {"limit": 1, "order": "id desc", "fields": ["check_out"]},
        ):
            last_attendance = cast(list[Any], response)[0]
        return last_attendance

    def add_checkout(self, att_id: str, time: datetime) -> None:
        """Add checkout to attendance."""
        self._execute_command(
            "hr.attendance",
            "write",
            [att_id, {"check_out": time.strftime("%Y-%m-%d %H:%M:%S")}],
            {},
        )

    def create_attendance(self, id: str, time: datetime) -> None:
        """Create new attendance for employee."""
        self._execute_command(
            "hr.attendance",
            "create",
            [{"employee_id": id, "check_in": time.strftime("%Y-%m-%d %H:%M:%S")}],
            {},
        )
