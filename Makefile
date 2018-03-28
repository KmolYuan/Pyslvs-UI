#Pyslvs Makefile

all: build

help:
	@echo ---Pyslvs Makefile Help---
	@echo make target:
	@echo - help: show this help message.
	@echo - all: build Pyslvs and test binary.
	@echo - build: build Pyslvs.
	@echo - build-kernel: build kernel only.
	@echo - build-cython: build cython kernel only.
	@echo - clean: clean executable file and PyInstaller items,
	@echo          will not delete kernel binary files.
	@echo - clean-kernel: clean up kernel binary files.
	@echo - clean-all: clean every binary files and executable file.
	@echo --------------------------

.PHONY: help build build-kernel clean clean-kernel clean-all

build-cython: core/libs/pyslvs_algorithm/*.pyx core/libs/pyslvs_topologic/*.pyx
	@echo ---Pyslvs generate Build---
	$(MAKE) -C core/libs/pyslvs_algorithm
	@echo ---Done---
	@echo ---Pyslvs topologic Build---
	$(MAKE) -C core/libs/pyslvs_topologic
	@echo ---Done---

build-kernel: build-cython
	@echo ---Python solvespace Build---
	$(MAKE) -C core/libs/python_solvespace
	@echo ---Done---

build: launch_pyslvs.py build-kernel
	@echo ---Pyslvs Build---
	@echo ---$(OS) Version---
ifeq ($(OS),Windows_NT)
	$(eval PYTHON = py$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")w)
	$(eval CPPYTHON = cp$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	$(eval PYQTPATH = $(shell python -c "import PyQt5, os, sys;sys.stdout.write(os.path.dirname(PyQt5.__file__))"))
	$(eval LARKPATH = $(shell python -c "import lark, os, sys;sys.stdout.write(os.path.dirname(lark.__file__))"))
	@echo --Python Version $(PYTHON)--
	pyinstaller -F $< -i ./icons/main.ico \
--path="$(PYQTPATH)\Qt\bin" \
--add-binary="core/libs/python_solvespace/libslvs.so;." \
--add-binary="core/libs/pyslvs_algorithm/de.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs_algorithm/firefly.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs_algorithm/planarlinkage.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs_algorithm/rga.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs_algorithm/tinycadlib.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/libs/pyslvs_topologic/topologic.$(CPPYTHON)-win_amd64.pyd;."
	$(eval PYSLVSVERSION = $(shell python -c "from core.info import VERSION; print(\"{}.{}.{}\".format(*VERSION))"))
	$(eval COMPILERVERSION = $(shell python -c "import platform; print(''.join(platform.python_compiler().split(\" \")[:2]).replace('.', '').lower())"))
	$(eval SYSVERSION = $(shell python -c "import platform; print(platform.machine().lower())"))
	rename .\dist\launch_pyslvs.exe pyslvs-$(PYSLVSVERSION).$(COMPILERVERSION)-$(SYSVERSION).exe
else
	$(eval PYTHON = py$(shell python3 -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	@echo --Python Version $(PYTHON)--
	@bash ./appimage_recipe.sh
endif
	@echo ---Done---

clean:
ifeq ($(OS),Windows_NT)
	-rd build /s /q
	-rd dist /s /q
	-del launch_pyslvs.spec
else
	-rm -f -r ENV
	-rm -f -r out
endif

clean-kernel:
	$(MAKE) -C core/libs/pyslvs_algorithm clean
	$(MAKE) -C core/libs/pyslvs_topologic clean
	$(MAKE) -C core/libs/python_solvespace clean

clean-all: clean-kernel clean
