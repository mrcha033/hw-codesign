FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG FREEROUTING_VERSION=2.2.4
ARG FREEROUTING_SHA256=f5ed374182900ccc78e473518bbb9f6b869f4a07159495f663a76f52bb10523b
ARG NODE_VERSION=22.22.3
ARG NODE_SHA256=2e5d13569282d016861fae7c8f935e741693c269101a5bebcf761a5376d1f99f
ARG ZEPHYR_VERSION=v4.2.0
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv kicad make git cmake ninja-build curl xz-utils \
    gcc-arm-none-eabi openjdk-21-jre-headless openscad freecad xvfb ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" -o /tmp/node.tar.xz \
    && echo "${NODE_SHA256}  /tmp/node.tar.xz" | sha256sum -c - \
    && tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 \
    && rm /tmp/node.tar.xz \
    && node --version \
    && npm --version

WORKDIR /opt/hw-platform
COPY pyproject.toml README.md package.json package-lock.json ./
COPY src ./src
COPY schemas ./schemas
COPY parts ./parts
RUN python3 -m pip install --break-system-packages --no-cache-dir '.[mcp,cad]' \
    west \
    && npm ci --ignore-scripts \
    && mkdir -p .toolchains/freerouting \
    && curl -fL "https://github.com/freerouting/freerouting/releases/download/v${FREEROUTING_VERSION}/freerouting-${FREEROUTING_VERSION}.jar" \
       -o ".toolchains/freerouting/freerouting-${FREEROUTING_VERSION}.jar" \
    && echo "${FREEROUTING_SHA256}  .toolchains/freerouting/freerouting-${FREEROUTING_VERSION}.jar" | sha256sum -c - \
    && git clone --depth 1 --branch "${ZEPHYR_VERSION}" https://github.com/zephyrproject-rtos/zephyr.git .toolchains/zephyr \
    && mkdir -p .toolchains/zephyr/modules/hal \
    && git clone https://github.com/zephyrproject-rtos/hal_stm32.git .toolchains/zephyr/modules/hal/stm32 \
    && git -C .toolchains/zephyr/modules/hal/stm32 checkout --detach 1e753266ddfb4b07a8a0b1ec566e9637ea45d5ef \
    && git clone https://github.com/zephyrproject-rtos/CMSIS_6.git .toolchains/zephyr/modules/hal/cmsis_6 \
    && git -C .toolchains/zephyr/modules/hal/cmsis_6 checkout --detach 06d952b6713a2ca41c9224a151 \
    && python3 -m pip install --break-system-packages --no-cache-dir -r .toolchains/zephyr/scripts/requirements-base.txt \
    && rm -rf .toolchains/zephyr/.git .toolchains/zephyr/modules/hal/stm32/.git .toolchains/zephyr/modules/hal/cmsis_6/.git

ENV HW_PLATFORM_ROOT=/workspace \
    HW_TOOLCHAIN_ROOT=/opt/hw-platform \
    HW_FREEROUTING_JAR=/opt/hw-platform/.toolchains/freerouting/freerouting-2.2.4.jar \
    HW_KICAD_PYTHON=/usr/bin/python3
WORKDIR /workspace
ENTRYPOINT ["hw"]
CMD ["--help"]
