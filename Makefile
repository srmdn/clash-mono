.PHONY: build check clean specimen

PYTHON ?= python3

build:
	@$(PYTHON) scripts/build.py

check:
	@$(PYTHON) scripts/check.py

specimen:
	@$(PYTHON) scripts/specimen.py

clean:
	@rm -rf build dist
