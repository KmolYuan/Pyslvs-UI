# Pyslvs Makefile

# author: Yuan Chang
# copyright: Copyright (C) 2016-2019
# license: AGPL
# email: pyslvs@gmail.com

LAUNCHSCRIPT = launch_pyslvs
USER_MODE ?= 0

ifeq ($(OS),Windows_NT)
    PY = python
else
    PY = python3
endif

PYVER_COMAND = "import sys; print('{v[0]}{v[1]}'.format(v=list(sys.version_info[:2])))"
PYSLVSVER_COMAND = "from core.libs import __version__; print(__version__)"
COMPILERVER_COMAND = "import platform; print(''.join(platform.python_compiler().split()[:2]).replace('.', '').lower())"
SYSVER_COMAND = "import platform; print(platform.machine().lower())"
ifeq ($(OS),Windows_NT)
    SHELL = cmd
    PYVER = $(shell $(PY) -c $(PYVER_COMAND))
    PYSLVSVER = $(shell $(PY) -c $(PYSLVSVER_COMAND))
    COMPILERVER = $(shell $(PY) -c $(COMPILERVER_COMAND))
    SYSVER = $(shell $(PY) -c $(SYSVER_COMAND))
else
    PYVER = $(shell $(PY) -c $(PYVER_COMAND))
    PYSLVSVER = $(shell $(PY) -c $(PYSLVSVER_COMAND))
    COMPILERVER = $(shell $(PY) -c $(COMPILERVER_COMAND))
    SYSVER = $(shell $(PY) -c $(SYSVER_COMAND))
endif
EXENAME = pyslvs-$(PYSLVSVER).$(COMPILERVER)-$(SYSVER)

.PHONY: help \
    build build-kernel build-pyslvs build-solvespace \
    test test-kernel test-pyslvs test-solvespace \
    clean clean-kernel clean-pyslvs clean-solvespace clean-all

all: test

help:
	@echo ---Pyslvs Makefile Help---
	@echo make target:
	@echo - help: show this help message.
	@echo - all: build Pyslvs and test binary.
	@echo - build: build Pyslvs executable file.
	@echo - build-kernel: build kernel only.
	@echo - build-pyslvs: build pyslvs kernel only.
	@echo - build-solvespace: build solvespace kernel only.
	@echo - clean: clean up executable file and PyInstaller items,
	@echo          but not to delete kernel binary files.
	@echo - clean-kernel: clean up kernel binary files.
	@echo - clean-pyslvs: clean up kernel binary files of pyslvs.
	@echo - clean-solvespace: clean up kernel binary files of solvespace.
	@echo - clean-all: clean every binary files and executable file.
	@echo --------------------------

build-pyslvs:
	@echo ---Pyslvs libraries Build---
	$(eval CMD = cd depend/pyslvs && $(PY) setup.py install)
ifeq ($(USER_MODE),1)
	$(CMD) --user
else
	$(CMD)
endif
	@echo ---Done---

build-solvespace:
	@echo ---Python Solvespace Build---
	$(MAKE) -C core/libs/python_solvespace
	@echo ---Done---

build-kernel: build-pyslvs build-solvespace

build: $(LAUNCHSCRIPT).py build-kernel test-kernel
	@echo ---Pyslvs Build---
	@echo ---$(OS) Version---
	@echo --Python Version $(PYVER)--
ifeq ($(OS),Windows_NT)
	pyinstaller -F $< -i ./icons/main.ico -n Pyslvs
	rename .\dist\Pyslvs.exe $(EXENAME).exe
else ifeq ($(shell uname),Darwin)
	pyinstaller -w -F $< -i ./icons/main.icns -n Pyslvs
	mv dist/Pyslvs dist/$(EXENAME)
	chmod +x dist/$(EXENAME)
	mv dist/Pyslvs.app dist/$(EXENAME).app
	zip -r dist/$(EXENAME).app.zip dist/$(EXENAME).app
else
	bash ./appimage_recipe.sh
endif
	@echo ---Done---

test-pyslvs:
	@echo ---Pyslvs libraries Test---
	cd depend/pyslvs && $(PY) tests/test_pyslvs.py
	@echo ---Done---

test-solvespace:
	@echo ---Python Solvespace Test---
	$(MAKE) -C core/libs/python_solvespace test
	@echo ---Done---

test-kernel: test-pyslvs test-solvespace

test: build
ifeq ($(OS),Windows_NT)
	./dist/$(EXENAME) --test
else ifeq ($(shell uname),Darwin)
	./dist/$(EXENAME) --test
else
	$(wildcard out/*.AppImage) --test
endif

clean:
ifeq ($(OS),Windows_NT)
	-rd build /s /q
	-rd dist /s /q
	-del *.spec
else ifeq ($(shell uname),Darwin)
	-rm -f -r build
	-rm -f -r dist
	-rm -f *.spec
else
	-rm -f -r ENV
	-rm -f -r out
endif

clean-pyslvs:
	$(MAKE) -C core/libs/pyslvs clean

clean-solvespace:
	$(MAKE) -C core/libs/python_solvespace clean

clean-kernel: clean-pyslvs clean-solvespace

clean-all: clean clean-kernel
