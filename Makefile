# Pyslvs Makefile

# author: Yuan Chang
# copyright: Copyright (C) 2016-2018
# license: AGPL
# email: pyslvs@gmail.com

LAUNCHSCRIPT = launch_pyslvs

ifeq ($(OS),Windows_NT)
    PYVER = $(shell python -c "import sys; t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2])); print(t)")
    PYSLVSVER = $(shell python -c "from core.info import __version__; print(\"{}.{:02}.{}\".format(*__version__))")
    COMPILERVER = $(shell python -c "import platform; print(''.join(platform.python_compiler().split(\" \")[:2]).replace('.', '').lower())")
    SYSVER = $(shell python -c "import platform; print(platform.machine().lower())")
else
    PYVER = $(shell python3 -c "import sys; t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2])); print(t)")
    PYSLVSVER = $(shell python3 -c "from core.info import __version__; print(\"{}.{:02}.{}\".format(*__version__))")
    COMPILERVER = $(shell python3 -c "import platform; print(''.join(platform.python_compiler().split(\" \")[:2]).replace('.', '').lower())")
    SYSVER = $(shell python3 -c "import platform; print(platform.machine().lower())")
endif

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
--hidden-import=PyQt5 \
--hidden-import=PyQt5.sip \
--hidden-import=PyQt5.QtPrintSupport \
--add-binary="core/libs/python_solvespace/libslvs.so;." \
--add-binary="core/libs/pyslvs/bfgs.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/de.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/firefly.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/planarlinkage.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/rga.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/tinycadlib.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/topologic.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/triangulation.cp$(PYVER)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/verify.cp$(PYVER)-win_amd64.pyd;."
	rename .\dist\Pyslvs.exe pyslvs-$(PYSLVSVER).$(COMPILERVER)-$(SYSVER).exe
else ifeq ($(shell uname),Darwin)
	@echo --Python Version $(PYVER)--
	pyinstaller -w -F $< -i ./icons/main.icns -n Pyslvs
	mv dist/Pyslvs.app dist/pyslvs-$(PYSLVSVER).$(COMPILERVER)-$(SYSVER).app
else
	@echo --Python Version $(PYVER)--
	bash ./appimage_recipe.sh
endif
	@echo ---Done---

test: build
ifeq ($(OS),Windows_NT)
	$(eval EXE = $(shell dir dist /b))
	./dist/$(EXE) --test
else ifeq ($(shell uname),Darwin)
	./dist/Pyslvs --test
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
