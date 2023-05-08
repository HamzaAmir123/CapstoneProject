# A Python Makefile

# Change if you use 'python' over 'python3'
PYTHON:=python3

# Python module locations
RUN:=src.main

# All are phony cmds
.PHONY: venv install dependencies clean run

default: install

venv:
	@echo "Creating virtual environment.."
	test -d venv || $(PYTHON) -m venv --upgrade-deps venv

dependencies: venv
	@echo "Installing packages.."
	. venv/bin/activate; $(PYTHON) -m pip install -Ur requirements.txt

install: dependencies
	@echo "Installing packages.."
	. venv/bin/activate; $(PYTHON) -m pip install --editable .

package:
	@echo "Packaging.."
	$(PYTHON) -m pip install .

test:
	. venv/bin/activate; $(PYTHON) -m pytest

run:
	. venv/bin/activate; roboviz

clean:
	rm -rf venv build roboviz.egg-info .pytest_cache
	find src -type d -name __pycache__ -exec rm -r {} \+
