# Pyslvs Makefile
# author: Yuan Chang
# copyright: Copyright (C) 2016-2019
# license: AGPL
# email: pyslvs@gmail.com

LAUNCHER = launch_pyslvs.py
PYSLVS_PATH = pyslvs

ifeq ($(OS),Windows_NT)
    PY = python
    SHELL = cmd
    _NEEDS_BUILD = true
else
    PY = python3
ifeq ($(shell uname),Darwin)
    _NEEDS_BUILD = true
endif
endif
PIP = $(PY) -m pip
ifdef _NEEDS_BUILD
    PYSLVSVER = $(shell $(PY) -c "from pyslvs import __version__; print(__version__)")
    COMPILERVER = $(shell $(PY) -c \
"import platform; print(''.join(platform.python_compiler().split()[:2]).replace('.', '').lower())")
    SYSVER = $(shell $(PY) -c "import platform; print(platform.machine().lower())")
    EXENAME = pyslvs-$(PYSLVSVER).$(COMPILERVER)-$(SYSVER)
endif

.PHONY: help install uninstall \
    build build-kernel test test-kernel clean clean-kernel clean-all

all: test

help:
	@echo Pyslvs Makefile Help
	@echo
	@echo make target:
	@echo   help: show this help message.
	@echo   all: build Pyslvs and test binary.
	@echo   build: build Pyslvs executable file.
	@echo   build-kernel: build kernel(s).
	@echo   install: install Pyslvs by setuptools.
	@echo   uninstall: uninstall Pyslvs by pip.
	@echo   clean: clean up executable file and PyInstaller items,
	@echo          but not to delete kernel binary files.
	@echo   clean-kernel: clean up kernel binary files.
	@echo   clean-all: clean every binary files and executable file.

build-kernel:
	@echo Build libraries
	-$(PIP) uninstall pyslvs -y
	cd $(PYSLVS_PATH) && $(PY) setup.py install
	@echo Done

ifdef _NEEDS_BUILD
_build: build-kernel test-kernel
else
_build:
endif

build: $(LAUNCHER) clean _build
	@echo Build executable for Python \
$(shell $(PY) -c "import platform; print(platform.python_version())")
ifeq ($(OS),Windows_NT)
	pyinstaller -F $< -i pyslvs_ui/icons/main.ico -n Pyslvs
	rename .\dist\Pyslvs.exe $(EXENAME).exe
else ifeq ($(shell uname),Darwin)
	pyinstaller -w -F $< -i pyslvs_ui/icons/main.icns -n Pyslvs
	mv dist/Pyslvs dist/$(EXENAME)
	chmod +x dist/$(EXENAME)
	mv dist/Pyslvs.app dist/$(EXENAME).app
	zip -r dist/$(EXENAME).app.zip dist/$(EXENAME).app
else
	bash platform/appimage_recipe.sh
endif
	@echo Done

install: build-kernel
	$(PY) setup.py install

uninstall:
	$(PIP) uninstall pyslvs-ui

test-kernel:
	@echo Test libraries
	cd $(PYSLVS_PATH) && $(PY) setup.py test
	@echo Done

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
	-rd pyslvs_ui.egg-info /s /q
	-del *.spec /q
else
	-rm -f -r build
	-rm -f -r dist
	-rm -f -r pyslvs_ui.egg-info
ifeq ($(shell uname),Darwin)
	-rm -f *.spec
else
	-rm -f -r ENV
	-rm -f -r out
endif
endif

clean-kernel:
	-$(PIP) uninstall pyslvs -y
	cd $(PYSLVS_PATH) && $(PY) setup.py clean --all
ifeq ($(OS),Windows_NT)
	-rd "$(PYSLVS_PATH)/dist" /s /q
	-rd "$(PYSLVS_PATH)/pyslvs.egg-info" /s /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del *.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del Adesign\*.cpp /q
else
	-rm -fr $(PYSLVS_PATH)/dist
	-rm -fr $(PYSLVS_PATH)/pyslvs.egg-info
	-rm -f $(PYSLVS_PATH)/pyslvs/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/Adesign/*.cpp
endif

clean-all: clean clean-kernel
