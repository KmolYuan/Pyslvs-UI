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
    NULL = NUL
else
    PY = python3
    NULL = /dev/null
endif
PIP = $(PY) -m pip

.PHONY: all help doc install uninstall \
    pack build test-pack test clean-pack clean clean-all

all: build

help:
	@echo Pyslvs Makefile Help
	@echo
	@echo make target:
	@echo   all: build kernel only.
	@echo   help: show this help message.
	@echo   doc: build the API documents.
	@echo   build-pack: build Pyslvs executable file.
	@echo   build: build kernel only.
	@echo   install: install Pyslvs by setuptools.
	@echo   uninstall: uninstall Pyslvs by pip.
	@echo   clean-pack: clean up executable file and PyInstaller items,
	@echo          but not to delete kernel binary files.
	@echo   clean: clean up kernel binary files.
	@echo   clean-all: clean every binary files and executable file.

doc:
ifeq (, $(shell which apimd > $(NULL)))
	$(PIP) install apimd
endif
	apimd Pyslvs=pyslvs Python-Solvespace=python_solvespace

build:
	@echo Build libraries
	-$(PIP) uninstall pyslvs -y
	cd $(PYSLVS_PATH) && $(PY) setup.py install
	@echo Done

pack: $(LAUNCHER) clean build
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

test:
	@echo Test libraries
	cd $(PYSLVS_PATH) && $(PY) setup.py test
	@echo Done

test-pack: pack
ifeq ($(OS), Windows_NT)
	$(wildcard dist/*.exe) test
else ifeq ($(shell uname), Darwin)
	$(wildcard dist/*.run) test
else
	$(wildcard out/*.AppImage) test
endif

clean:
	-$(PIP) uninstall pyslvs -y
	cd $(PYSLVS_PATH) && $(PY) setup.py clean --all
ifeq ($(OS), Windows_NT)
	-rd "$(PYSLVS_PATH)/dist" /s /q
	-rd "$(PYSLVS_PATH)/pyslvs.egg-info" /s /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del *.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del *.pyd /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del graph\*.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del graph\*.pyd /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del metaheuristics\*.cpp /q
	-cd "$(PYSLVS_PATH)/pyslvs" && del metaheuristics\*.pyd /q
else
	-rm -fr $(PYSLVS_PATH)/dist
	-rm -fr $(PYSLVS_PATH)/pyslvs.egg-info
	-rm -f $(PYSLVS_PATH)/pyslvs/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/*.so
	-rm -f $(PYSLVS_PATH)/pyslvs/graph/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/graph/*.so
	-rm -f $(PYSLVS_PATH)/pyslvs/metaheuristics/*.cpp
	-rm -f $(PYSLVS_PATH)/pyslvs/metaheuristics/*.so
endif

clean-pack:
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

clean-all: clean-pack clean
