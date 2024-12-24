PYTHON := python
VENV_NAME := .venv

## project name
PROJECT := example_publish_pypi

## section name in ~/.pypirc
## https://packaging.python.org/en/latest/specifications/pypirc/#the-pypirc-file
# REPOSITORY := testpypi
REPOSITORY := pypi

help: ## show this help
	@test -f .external/makefile-doc.awk || \
	wget --quiet -P .external github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
	@awk -f .external/makefile-doc.awk $(MAKEFILE_LIST)

## editable install in venv
install-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install -e .[dev]

setup-venv: ## setup a python venv
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip

## create dist
dist-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install build && ${PYTHON} -m build

publish: ##! publish to PyPi
	pip install build && ${PYTHON} -m build && pip install twine && \
	twine upload --repository $(REPOSITORY) dist/* --verbose

clean: ## clean generated files
	@rm -rf dist .venv
	@rm -rf src/$(PROJECT).egg-info
	@rm -rf src/$(PROJECT)/_version.py
	@rm -rf .external
