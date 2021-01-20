# Pyslvs Makefile
# author: Yuan Chang
# copyright: Copyright (C) 2016-2021
# license: AGPL
# email: pyslvs@gmail.com

ifeq ($(OS), Windows_NT)
    PY = python
    SHELL = cmd
    NULL = NUL
else
    PY = python3
    NULL = /dev/null
endif
PIP = $(PY) -m pip

.PHONY: all help doc ui qrc install uninstall build pack test-pack

all: build

help:
	@echo Pyslvs Makefile Help
	@echo
	@echo "make target:"
	@echo "  all: build kernel only."
	@echo "  help: show this help message."
	@echo "  doc: build the API documents."
	@echo "  ui: compile ui files."
	@echo "  qrc: compile qrc files."
	@echo "  pack: build Pyslvs executable file."
	@echo "  build: build kernel only."
	@echo "  install: install Pyslvs by setuptools."
	@echo "  uninstall: uninstall Pyslvs by pip."
	@echo "  test-pack: run pack self-check."

doc: build
	apimd Pyslvs=pyslvs Python-Solvespace=python_solvespace

ui:
	$(PY) compile_resource.py --ui

qrc:
	$(PY) compile_resource.py --qrc

build:
	@echo Build libraries
	-$(PIP) uninstall pyslvs -y
	$(PIP) install -e .
	@echo Done

pack: clean build
	@echo Build executable for Python \
$(shell $(PY) -c "import platform; print(platform.python_version())")
ifeq ($(OS), Windows_NT)
	bash platform/pyinstaller_recipe.sh
else ifeq ($(shell uname), Darwin)
	bash platform/pyinstaller_recipe.sh
else
	bash platform/appimage_recipe.sh
endif
	@echo Done

install: build
	$(PY) setup.py install

uninstall:
	$(PIP) uninstall pyslvs-ui pyslvs python-solvespace

test-pack: pack
ifeq ($(OS), Windows_NT)
	$(wildcard dist/*.exe) test
else ifeq ($(shell uname), Darwin)
	$(wildcard dist/*.run) test
else
	$(wildcard out/*.AppImage) test
endif
