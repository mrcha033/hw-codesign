.PHONY: install toolchains test lint sample check-sample docker-build

install:
	python3 -m pip install '.[dev,mcp]'

toolchains:
	bash scripts/bootstrap_toolchains.sh

test:
	python3 -m pytest

sample:
	hw --root . create-project quadruped_robot_controller

check-sample:
	hw --root . design-until-release quadruped_robot_controller --external

docker-build:
	docker build -f docker/Dockerfile -t hw-codesign-platform:0.1.0 .
