######################################################
## Defaults
######################################################

SHELL=bash

######################################################
## Setup
######################################################

setup: venv venv/requirements.txt

venv:
	virtualenv venv

venv/requirements.txt: venv requirements.txt
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip list --outdated
	cp requirements.txt venv/requirements.txt
