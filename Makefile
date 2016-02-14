######################################################
## Defaults
######################################################

SHELL=bash

######################################################
## Setup
######################################################

.PHONY: clean setup

clean:
	rm -rf build
	rm -rf venv

setup: venv venv/requirements.txt

venv:
	virtualenv venv

venv/requirements.txt: venv requirements.txt
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip list --outdated
	cp requirements.txt venv/requirements.txt


######################################################
## Testing
######################################################

.PHONY: test test-unit

test: test-unit

test-unit: setup
	@ echo "Running unit tests"
	@ . venv/bin/activate; flake8 --max-line-length=100 test/unit
	@ . venv/bin/activate; nosetests test/unit