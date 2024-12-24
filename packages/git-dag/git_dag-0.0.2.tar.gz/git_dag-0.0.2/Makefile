PYTHON := python
VENV_NAME := .venv
PYLINT := pylint
HTML_DIR := docs/sphinx/build/html

help: ## show this help
	@test -f .external/makefile-doc.awk || \
	wget --quiet -P .external github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
	@awk -f .external/makefile-doc.awk $(MAKEFILE_LIST)

# ----------------------------------------------------------------

## Lint code
lint: lint-run

## Run mypy check
mypy: mypy-run

## Editable install in venv
install-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install -e .[dev]

pre-commit: ## Execute pre-commit on all files
	@pre-commit run -a

# ----------------------------------------------------------------

lint-run:
	$(PYLINT) src/git_dag/* > .pylint_report.json || exit 0
	pylint_report .pylint_report.json -o .pylint_report.html

mypy-run:
	mypy || exit 0

setup-venv:
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip

dist-local: setup-venv
	. ${VENV_NAME}/bin/activate && pip install build && ${PYTHON} -m build

publish: ##! Publish to PyPi
	pip install build && ${PYTHON} -m build && pip install twine && \
	twine upload dist/* --verbose

clean: ##! Clean all
	rm -rf build
	rm -rf .mypy_cache
	rm -rf src/git_dag.egg-info
	rm -rf src/git_dag/_version.py
	find . -name "__pycache__" | xargs rm -rf
	rm -rf *.egg-info dist .pytest_cache .coverage
	rm -rf .external
	rm -rf .venv
	rm -rf .pylint_report*
