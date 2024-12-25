"""Exceptions raised by Odoo plugin."""


class OdooError(Exception):
    """Raise error if authentication fails."""


class InvalidAuth(OdooError):
    """Raise error if authentication fails."""


class ConnectError(OdooError):
    """Raise error if connection fails."""


class ConfigError(OdooError):
    """Raise error if user doesn't have required privileges."""


class RequestError(OdooError):
    """Raise error if bad request."""
