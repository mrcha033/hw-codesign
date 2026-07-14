from __future__ import annotations

import os

from hw_codesign.stdio import redirect_tool_stdout_to_stderr


def test_tool_stdout_guard_redirects_python_and_native_output(capfd):
    with redirect_tool_stdout_to_stderr():
        print("python CAD log")
        os.write(1, b"native CAD log\n")

    captured = capfd.readouterr()
    assert captured.out == ""
    assert "python CAD log" in captured.err
    assert "native CAD log" in captured.err
