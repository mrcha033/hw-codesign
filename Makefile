.PHONY: install toolchains test lint sample check-sample docker-build

install:
	uv sync --locked --extra dev --extra mcp

toolchains:
	bash scripts/bootstrap_toolchains.sh

test:
	uv run pytest

lint:
	uv run ruff check src cli server tests

sample:
	hw --root . create-project quadruped_robot_controller

check-sample:
	hw --root . design-until-release quadruped_robot_controller --external

docker-build:
	docker build -f docker/Dockerfile -t hw-codesign-platform:$(shell grep '^version' pyproject.toml | head -1 | cut -d'"' -f2) .
