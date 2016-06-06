######################################################
## Defaults
######################################################

SHELL=bash

######################################################
## Setup
######################################################

.PHONY: clean setup lint

clean: logs
	rm -rf ./build
	rm -rf ./venv

logs:
	rm -rf ./logs
	mkdir ./logs

setup: venv venv/requirements.txt lint

venv:
	virtualenv venv

venv/requirements.txt: venv requirements.txt
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip list --outdated
	cp requirements.txt venv/requirements.txt

lint:
	@ . venv/bin/activate; flake8 ./*.py fetch utils test/unit
	@ . venv/bin/activate; radon cc -a -nc -e "venv/*" ./


######################################################
## Testing
######################################################

.PHONY: test test-unit test-integration

test: test-unit

test-unit: setup
	@ echo "Running unit tests"
	@ . venv/bin/activate; nosetests test/unit

test-integration: setup
	@ echo "Running integration tests"
	@ . venv/bin/activate; nosetests test/integration


######################################################
## Running
######################################################

.PHONY: run

run: setup
	@ echo "Running"
	@ . venv/bin/activate; ./bee.py

restore: setup
	@ echo "Restoring"
	@ . venv/bin/activate; ./beerestore.py
