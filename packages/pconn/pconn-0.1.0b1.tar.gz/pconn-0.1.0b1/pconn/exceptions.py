"""Exceptions raised by plugins."""


class PConnError(Exception):
    """General Platform Connecters exception occurred."""


class CertificateError(PConnError):
    """Raise Certificate error if certificate is not found."""


class PluginEntryError(PConnError):
    """General Plugin related error."""

    def __init__(self, message: str, reason: str | None = None) -> None:
        """Init the error."""
        super().__init__(message)
        self.reason = reason


class PlatformNotReady(PluginEntryError):
    """Raise exception if platform is not ready."""


class PluginEntryNotReady(PluginEntryError):
    """Raise plugin error."""


class UnknownPluginAction(PluginEntryError):
    """Raise error if action is unknown."""


class PluginActionError(PConnError):
    """Raised by registered action callbacks."""


class DependencyError(PConnError):
    """Raised when dependencies cannot be setup."""

    def __init__(self, failed_dependencies: list[str]) -> None:
        """Initialize error."""
        super().__init__(
            f"Could not setup dependencies: {', '.join(failed_dependencies)}",
        )
        self.failed_dependencies = failed_dependencies
