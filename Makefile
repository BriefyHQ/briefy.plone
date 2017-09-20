.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	bin/code-analysis

stop_containers: ## stop and remove docker containers
	# s3
	docker ps|grep 's3' |awk '{ print $$1 }'|xargs docker stop
	docker ps -a|grep 's3' |awk '{ print $$1 }'|xargs docker rm
	# mysql
	docker ps|grep 'briefy-plone-test' |awk '{ print $$1}'|xargs docker stop
	docker ps -a|grep 'briefy-plone-test' |awk '{ print $$1}'|xargs docker rm

start_containers: stop_containers ## stop, remove and recreate docker containers
	# s3
	docker run -d -p 5000:5000 --name s3 briefy/aws-test:latest s3
	# mysql
	docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cms --name briefy-plone-test mysql:5.7
	sleep 5

test: lint ## run tests quickly with the default Python
	bin/test
