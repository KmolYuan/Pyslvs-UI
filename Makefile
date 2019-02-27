# Pyslvs Makefile

# author: Yuan Chang
# copyright: Copyright (C) 2016-2019
# license: AGPL
# email: pyslvs@gmail.com

LAUNCHSCRIPT = launch_pyslvs

PYVER_COMAND = "import sys; print('{v[0]}{v[1]}'.format(v=list(sys.version_info[:2])))"
PYSLVSVER_COMAND = "from core.info import __version_str__; print(__version_str__)"
COMPILERVER_COMAND = "import platform; print(''.join(platform.python_compiler().split()[:2]).replace('.', '').lower())"
SYSVER_COMAND = "import platform; print(platform.machine().lower())"
ifeq ($(OS),Windows_NT)
    SHELL = cmd
    PYVER = $(shell python -c $(PYVER_COMAND))
    PYSLVSVER = $(shell python -c $(PYSLVSVER_COMAND))
    COMPILERVER = $(shell python -c $(COMPILERVER_COMAND))
    SYSVER = $(shell python -c $(SYSVER_COMAND))
else
    PYVER = $(shell python3 -c $(PYVER_COMAND))
    PYSLVSVER = $(shell python3 -c $(PYSLVSVER_COMAND))
    COMPILERVER = $(shell python3 -c $(COMPILERVER_COMAND))
    SYSVER = $(shell python3 -c $(SYSVER_COMAND))
endif
EXENAME = pyslvs-$(PYSLVSVER).$(COMPILERVER)-$(SYSVER)

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

.PHONY: help \
    build build-kernel build-pyslvs build-solvespace \
    clean clean-kernel clean-pyslvs clean-solvespace clean-all

build-pyslvs:
	@echo ---Pyslvs libraries Build---
	$(MAKE) -C core/libs/pyslvs build
	@echo ---Done---

build-solvespace:
	@echo ---Python solvespace Build---
	$(MAKE) -C core/libs/python_solvespace
	@echo ---Done---

build-kernel: build-pyslvs build-solvespace

build: $(LAUNCHSCRIPT).py build-kernel
	@echo ---Pyslvs Build---
	@echo ---$(OS) Version---
ifeq ($(OS),Windows_NT)
	@echo --Python Version $(PYVER)--
	pyinstaller -F $< -i ./icons/main.ico -n Pyslvs \
--add-binary="core/libs/python_solvespace/libslvs.so;."
	rename .\dist\Pyslvs.exe $(EXENAME).exe
else ifeq ($(shell uname),Darwin)
	@echo --Python Version $(PYVER)--
	pyinstaller -w -F $< -i ./icons/main.icns -n Pyslvs
	mv dist/Pyslvs dist/$(EXENAME)
	chmod +x dist/$(EXENAME)
	mv dist/Pyslvs.app dist/$(EXENAME).app
	zip -r dist/$(EXENAME).app.zip dist/$(EXENAME).app
else
	@echo --Python Version $(PYVER)--
	bash ./appimage_recipe.sh
endif
	@echo ---Done---

test: build
ifeq ($(OS),Windows_NT)
	./dist/$(EXENAME) --test
else ifeq ($(shell uname),Darwin)
	./dist/$(EXENAME) --test
else
	$(eval APPIMAGE = $(shell ls -1 out))
	./out/$(APPIMAGE) --test
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
