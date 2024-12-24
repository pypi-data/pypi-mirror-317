PYTHON := python
VENV_NAME := .venv

help: ## show this help
	@test -f .external/makefile-doc.awk || \
	wget --quiet -P .external github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
	@awk -f .external/makefile-doc.awk $(MAKEFILE_LIST)

## Editable install in venv
install-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install -e .[dev]

setup-venv:
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip

dist-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install build && ${PYTHON} -m build

publish: ##! Publish to PyPi
	pip install build && ${PYTHON} -m build && pip install twine && \
	twine upload dist/* --verbose

clean:
	rm -rf src/directly_dash/_version.py
	rm -rf dist
