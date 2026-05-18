.PHONY: build check clean specimen smoke

PYTHON ?= python3

build:
	@$(PYTHON) scripts/build.py

check:
	@$(PYTHON) scripts/check.py

specimen:
	@$(PYTHON) scripts/specimen.py

smoke:
	@$(PYTHON) scripts/smoke.py

clean:
	@rm -rf build dist
