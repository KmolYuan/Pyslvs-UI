# Pyslvs Makefile
# author: Yuan Chang
# copyright: Copyright (C) 2016-2020
# license: AGPL
# email: pyslvs@gmail.com

LAUNCHER = launch_pyslvs.py
PYSLVS_PATH = pyslvs

ifeq ($(OS), Windows_NT)
    PY = python
    SHELL = cmd
else
    PY = python3
endif
PIP = $(PY) -m pip

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

build: $(LAUNCHER) clean
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

install: build-kernel
	$(PY) setup.py install

uninstall:
	$(PIP) uninstall pyslvs-ui

test-kernel:
	@echo Test libraries
	cd $(PYSLVS_PATH) && $(PY) setup.py test
	@echo Done

test: build
ifeq ($(OS), Windows_NT)
	$(wildcard dist/*.exe) --test
else ifeq ($(shell uname), Darwin)
	$(wildcard dist/*.run) --test
else
	$(wildcard out/*.AppImage) --test
endif

clean:
ifeq ($(OS), Windows_NT)
	-rd build /s /q
	-rd dist /s /q
	-rd pyslvs_ui.egg-info /s /q
	-rd ENV /s /q
	-del *.spec /q
else
	-rm -f -r build
	-rm -f -r dist
	-rm -f -r pyslvs_ui.egg-info
	-rm -f -r ENV
ifeq ($(shell uname), Darwin)
	-rm -f *.spec
else
	-rm -f -r out
endif
endif

clean-kernel:
	-$(PIP) uninstall pyslvs -y
	cd $(PYSLVS_PATH) && $(PY) setup.py clean --all
ifeq ($(OS), Windows_NT)
	-rd "$(PYSLVS_PATH)/dist" /s /q
	-rd "$(PYSLVS_PATH)/pyslvs.egg-info" /s /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del *.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del *.pyd /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del metaheuristics\*.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del metaheuristics\*.pyd /q
else
	-rm -fr $(PYSLVS_PATH)/dist
	-rm -fr $(PYSLVS_PATH)/pyslvs.egg-info
	-rm -f $(PYSLVS_PATH)/pyslvs/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/*.so
	-rm -f $(PYSLVS_PATH)/pyslvs/metaheuristics/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/metaheuristics/*.so
endif

clean-all: clean clean-kernel
