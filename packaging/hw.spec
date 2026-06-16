# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — builds hw and hw-mcp as standalone onefiles."""

from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

repo_root = Path(SPECPATH).parent

# ── data files ──────────────────────────────────────────────────────────────
base_datas = [
    (str(repo_root / "schemas"), "schemas"),
    (str(repo_root / "parts"), "parts"),
    # templates accessed via importlib.resources — must be explicit with editable installs
    (str(repo_root / "src" / "hw_codesign" / "templates"), "hw_codesign/templates"),
]

mcp_datas, mcp_binaries, mcp_hiddenimports = collect_all(
    "mcp",
    filter_submodules=lambda name: "mcp.cli" not in name,
    on_error="warn",
)
ksa_datas, ksa_binaries, ksa_hiddenimports = collect_all("kicad_sch_api")
hw_datas, hw_binaries, hw_hiddenimports = collect_all("hw_codesign")
js_hidden = collect_submodules("jsonschema")

all_datas = base_datas + mcp_datas + ksa_datas + hw_datas
all_binaries = mcp_binaries + ksa_binaries + hw_binaries
all_hidden = (
    mcp_hiddenimports
    + ksa_hiddenimports
    + hw_hiddenimports
    + js_hidden
    + ["yaml", "jsonschema", "jsonschema.validators", "hw_codesign.templates"]
)

# ── hw CLI ───────────────────────────────────────────────────────────────────
a_hw = Analysis(
    [str(repo_root / "packaging" / "entry_hw.py")],
    pathex=[str(repo_root / "src")],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["cadquery", "cadquery_ocp", "OCP", "tkinter", "matplotlib", "numpy"],
    noarchive=False,
)
pyz_hw = PYZ(a_hw.pure)
exe_hw = EXE(
    pyz_hw,
    a_hw.scripts,
    a_hw.binaries,
    a_hw.zipfiles,
    a_hw.datas,
    [],
    name="hw",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ── hw-mcp server ─────────────────────────────────────────────────────────
a_mcp = Analysis(
    [str(repo_root / "packaging" / "entry_hw_mcp.py")],
    pathex=[str(repo_root / "src")],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["cadquery", "cadquery_ocp", "OCP", "tkinter", "matplotlib", "numpy"],
    noarchive=False,
)
pyz_mcp = PYZ(a_mcp.pure)
exe_mcp = EXE(
    pyz_mcp,
    a_mcp.scripts,
    a_mcp.binaries,
    a_mcp.zipfiles,
    a_mcp.datas,
    [],
    name="hw-mcp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
