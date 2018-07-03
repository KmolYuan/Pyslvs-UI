#Pyslvs Makefile

#author: Yuan Chang
#copyright: Copyright (C) 2016-2018
#license: AGPL
#email: pyslvs@gmail.com

LAUNCHSCRIPT = launch_pyslvs

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
	$(eval PYTHON = py$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")w)
	$(eval CPPYTHON = cp$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	@echo --Python Version $(PYTHON)--
	pyinstaller -F $< -i ./icons/main.ico \
--hidden-import=PyQt5 \
--hidden-import=PyQt5.sip \
--hidden-import=PyQt5.QtPrintSupport \
--add-binary="core/libs/python_solvespace/libslvs.so;." \
--add-binary="core/libs/pyslvs/bfgs.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/de.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/firefly.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/planarlinkage.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/rga.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/tinycadlib.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/topologic.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/triangulation.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs/verify.$(CPPYTHON)-win_amd64.pyd;."
	$(eval PYSLVSVERSION = $(shell python -c "from core.info import __version__; print(\"{}.{}.{}\".format(*__version__))"))
	$(eval COMPILERVERSION = $(shell python -c "import platform; print(''.join(platform.python_compiler().split(\" \")[:2]).replace('.', '').lower())"))
	$(eval SYSVERSION = $(shell python -c "import platform; print(platform.machine().lower())"))
	rename .\dist\$(LAUNCHSCRIPT).exe pyslvs-$(PYSLVSVERSION).$(COMPILERVERSION)-$(SYSVERSION).exe
else
	$(eval PYTHON = py$(shell python3 -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	@echo --Python Version $(PYTHON)--
	bash ./appimage_recipe.sh
endif
	@echo ---Done---

test: build
ifeq ($(OS),Windows_NT)
	$(eval EXE = $(shell dir dist /b))
	./dist/$(EXE) --test
else
	$(eval APPIMAGE = $(shell ls -1 out))
	./out/$(APPIMAGE) --test
endif

clean:
ifeq ($(OS),Windows_NT)
	-rd build /s /q
	-rd dist /s /q
	-del launch_pyslvs.spec
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
