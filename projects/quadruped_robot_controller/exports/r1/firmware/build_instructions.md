# Firmware Build

Reference verification: `cmake -S firmware/reference -B build -G Ninja && cmake --build build && ctest --test-dir build`.

Zephyr target: `west build -b robot_controller firmware/zephyr/app`.
