from __future__ import annotations


class HardwarePlatformError(Exception):
    """Base error for user-facing platform failures."""


class ProjectNotFoundError(HardwarePlatformError):
    pass


class InvalidProjectNameError(HardwarePlatformError):
    pass


class UnsafeChangeError(HardwarePlatformError):
    pass

