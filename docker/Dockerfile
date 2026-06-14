FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv nodejs npm kicad make git cmake ninja-build \
    gcc-arm-none-eabi openscad freecad xvfb ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/hw-platform
COPY pyproject.toml README.md package.json package-lock.json ./
COPY src ./src
COPY schemas ./schemas
COPY parts ./parts
RUN python3 -m pip install --break-system-packages --no-cache-dir '.[mcp,cad]' \
    && npm ci --ignore-scripts

ENV HW_PLATFORM_ROOT=/workspace
WORKDIR /workspace
ENTRYPOINT ["hw"]
