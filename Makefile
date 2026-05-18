.PHONY: build check clean

PYTHON ?= python3

build:
	@$(PYTHON) scripts/build.py

check:
	@$(PYTHON) scripts/check.py

clean:
	@rm -rf build dist
