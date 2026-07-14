from __future__ import annotations

import contextlib
import os
import sys
import threading
from collections.abc import Iterator

_STDOUT_GUARD = threading.RLock()


@contextlib.contextmanager
def redirect_tool_stdout_to_stderr() -> Iterator[None]:
    """Keep accidental Python and native-library output off MCP stdout.

    MCP's stdio transport owns file descriptor 1. Tool handlers may call CAD/EDA
    libraries that write through either ``print`` or the native stdout file
    descriptor, so both layers are redirected for the duration of a handler.
    The descriptor is restored before FastMCP serializes the JSON-RPC result.
    """

    with _STDOUT_GUARD:
        saved_stdout_fd: int | None = None
        try:
            try:
                sys.stdout.flush()
                sys.stderr.flush()
                saved_stdout_fd = os.dup(1)
                os.dup2(2, 1)
            except OSError:
                saved_stdout_fd = None
            with contextlib.redirect_stdout(sys.stderr):
                yield
        finally:
            if saved_stdout_fd is not None:
                try:
                    sys.stderr.flush()
                    os.dup2(saved_stdout_fd, 1)
                finally:
                    os.close(saved_stdout_fd)
