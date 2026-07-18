from __future__ import annotations

import os

from hw_codesign import __version__
from hw_codesign.mcp_server import create_server
from hw_codesign.stdio import redirect_tool_stdout_to_stderr


def test_tool_stdout_guard_redirects_python_and_native_output(capfd):
    with redirect_tool_stdout_to_stderr():
        print("python CAD log")
        os.write(1, b"native CAD log\n")

    captured = capfd.readouterr()
    assert captured.out == ""
    assert "python CAD log" in captured.err
    assert "native CAD log" in captured.err


def test_mcp_server_advertises_application_version(tmp_path):
    server = create_server(tmp_path)

    assert server._mcp_server.name == "hw-codesign"
    assert server._mcp_server.version == __version__
