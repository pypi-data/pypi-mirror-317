# Makefile by Davide Ponzini

NAME=dav-tools
PY=python


prepare: test documentation
	:

install: uninstall build
	$(PY) -m pip install ./dist/*.whl

build:
	sudo rm -rf dist/
	$(PY) -m build

uninstall:
	$(PY) -m pip uninstall -y $(NAME)

documentation:
	make html -C docs/

test: install
	$(PY) -m pytest

requirements.txt:
	$(PY) -m pip install pipreqs
	$(PY) -m pipreqs --mode no-pin --force

required-packages: requirements.txt
	$(PY) -m pip install --upgrade build autoapi pytest -r requirements.txt

upload: prepare
	$(PY) -m pip install --upgrade twine
	$(PY) -m twine upload --verbose dist/*

download: uninstall
	$(PY) -m pip install $(NAME)

