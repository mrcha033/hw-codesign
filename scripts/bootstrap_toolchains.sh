#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$ROOT/.toolchains"
ZEPHYR="$TOOLS/zephyr"
JAVA="$TOOLS/java25"
FREEROUTING="$TOOLS/freerouting/freerouting-2.2.4.jar"
HAL_RPI_PICO_REVISION="7b57b24588797e6e7bf18b6bda168e6b96374264"

require_complete_arm_toolchain() {
  local compiler specs
  compiler="$(command -v arm-none-eabi-gcc || true)"
  if [[ -z "$compiler" ]]; then
    cat >&2 <<'EOF'
A complete Arm GNU Toolchain is required for native Zephyr builds.
Install the official Arm GNU Toolchain, then prepend its bin directory to PATH.
The compiler must include Arm newlib and nosys.specs; the Homebrew
arm-none-eabi-gcc formula alone is not sufficient.

Verify the installation with:
  specs="$(arm-none-eabi-gcc -print-file-name=nosys.specs)"
  test "$specs" != nosys.specs && test -f "$specs"

Official downloads: https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
Alternatively, use docker/Dockerfile, which provisions GCC and newlib together.
EOF
    exit 1
  fi

  specs="$("$compiler" -print-file-name=nosys.specs)"
  if [[ "$specs" == "nosys.specs" || ! -f "$specs" ]]; then
    cat >&2 <<EOF
The Arm compiler at $compiler is incomplete: nosys.specs was not found.
Install the official Arm GNU Toolchain (compiler + Arm newlib), prepend its bin
directory to PATH, and rerun this script. The Homebrew arm-none-eabi-gcc
formula alone is not sufficient.

Official downloads: https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
Alternatively, use docker/Dockerfile, which provisions GCC and newlib together.
EOF
    exit 1
  fi

  echo "Arm GNU Toolchain ready: $compiler (nosys.specs: $specs)"
}

command -v brew >/dev/null || { echo "Homebrew is required on macOS" >&2; exit 1; }
if [[ ! -x /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli ]]; then
  brew install --cask kicad
fi
require_complete_arm_toolchain
command -v ato >/dev/null || brew install atopile
command -v curl >/dev/null || { echo "curl is required" >&2; exit 1; }
command -v node >/dev/null || brew install node@22
command -v npm >/dev/null || { echo "npm is required" >&2; exit 1; }

command -v uv >/dev/null || { echo "uv is required: https://docs.astral.sh/uv/getting-started/installation/" >&2; exit 1; }
uv sync --locked --extra dev --extra mcp --extra cad
uv pip install west
npm --prefix "$ROOT" ci --ignore-scripts

mkdir -p "$TOOLS"
if [[ "$(uname -m)" != "arm64" ]]; then
  echo "The pinned local JRE bootstrap currently supports macOS arm64 only." >&2
  exit 1
fi
if [[ ! -x "$JAVA/Contents/Home/bin/java" ]]; then
  archive="$(mktemp)"
  curl -fL 'https://api.adoptium.net/v3/binary/version/jdk-25.0.3%2B9/mac/aarch64/jre/hotspot/normal/eclipse' -o "$archive"
  echo "287cc80077dc2ffd0e5733ba238f92206a84c26bef33e6881a23c213e4c35af4  $archive" | shasum -a 256 -c -
  mkdir -p "$JAVA"
  tar -xzf "$archive" -C "$JAVA" --strip-components=1
  rm -f "$archive"
fi
if [[ ! -f "$FREEROUTING" ]]; then
  mkdir -p "$(dirname "$FREEROUTING")"
  curl -fL 'https://github.com/freerouting/freerouting/releases/download/v2.2.4/freerouting-2.2.4.jar' -o "$FREEROUTING"
fi
echo "f5ed374182900ccc78e473518bbb9f6b869f4a07159495f663a76f52bb10523b  $FREEROUTING" | shasum -a 256 -c -
if [[ ! -d "$ZEPHYR/.git" ]]; then
  git clone --depth 1 --branch v4.2.0 https://github.com/zephyrproject-rtos/zephyr.git "$ZEPHYR"
fi
uv pip install -r "$ZEPHYR/scripts/requirements-base.txt"

clone_at() {
  local url="$1" path="$2" revision="$3"
  if [[ ! -d "$path/.git" ]]; then
    git clone --filter=blob:none "$url" "$path"
  fi
  git -C "$path" checkout --detach "$revision"
}

mkdir -p "$ZEPHYR/modules/hal"
clone_at https://github.com/zephyrproject-rtos/hal_stm32.git "$ZEPHYR/modules/hal/stm32" 1e753266ddfb4b07a8a0b1ec566e9637ea45d5ef
clone_at https://github.com/zephyrproject-rtos/CMSIS_6.git "$ZEPHYR/modules/hal/cmsis_6" 06d952b6713a2ca41c9224a62075e4059402a151
clone_at https://github.com/zephyrproject-rtos/hal_rpi_pico.git "$ZEPHYR/modules/hal/rpi_pico" "$HAL_RPI_PICO_REVISION"

echo "Pinned tscircuit, KiCad, Freerouting, OpenJDK, and Zephyr toolchains are ready."
