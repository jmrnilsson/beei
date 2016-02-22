######################################################
## Defaults
######################################################

SHELL=bash

######################################################
## Setup
######################################################

.PHONY: clean setup

clean:
	rm -rf ./build
	rm -rf ./venv
	rm -rf ./logs
	mkdir ./logs

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

.PHONY: test test-unit test-integration

test: test-unit

test-unit: setup
	@ echo "Running unit tests"
	@ . venv/bin/activate; flake8 --max-line-length=100 test/unit
	@ . venv/bin/activate; nosetests test/unit

test-integration: setup
	@ echo "Running integration tests"
	@ . venv/bin/activate; nosetests test/integration


######################################################
## Running
######################################################

.PHONY: run

run:
	@ echo "Running"
	@ . venv/bin/activate; ./bee.py
