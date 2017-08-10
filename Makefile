#Pyslvs Makefile

all: build run

help:
	@echo ---Pyslvs Makefile Help---
	@echo make target:
	@echo - help: show this help message.
	@echo - all: build Pyslvs and test binary.
	@echo - build: build Pyslvs.
	@echo - build-kernel: build kernel only.
	@echo - deb (Ubuntu only): build and pack up as debian installer.
	@echo - clean: clean executable file and PyInstaller items,
	@echo          will not delete kernel binary files.
	@echo - clean-kernel: clean up kernel binary files.
	@echo - clean-all: clean every binary files and executable file.
	@echo --------------------------

.PHONY: help build build-kernel deb clean clean-kernel clean-all

build-kernel: core/kernel/pyslvs_algorithm/*.pyx
	@echo ---Pyslvs generate Build---
	$(MAKE) -C core/kernel/pyslvs_algorithm
	@echo ---Done---
	@echo ---Python solvespace Build---
	$(MAKE) -C core/kernel/python_solvespace
	@echo ---Done---

build: launch_pyslvs.py build-kernel
	@echo ---Pyslvs Build---
	@echo ---$(OS) Version---
ifeq ($(OS),Windows_NT)
	$(eval PYTHON = py$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")w)
	$(eval CPPYTHON = cp$(shell python -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	$(eval PYQTPATH = $(shell python -c "import PyQt5, os, sys;sys.stdout.write(os.path.dirname(PyQt5.__file__))"))
	@echo --Python Version $(PYTHON)--
	pyinstaller -F $< -i ./icons/main_big.ico \
--path="$(PYQTPATH)\Qt\bin" \
--add-binary="core/kernel/python_solvespace/libslvs.so;." \
--add-binary="core/kernel/pyslvs_algorithm/de.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/kernel/pyslvs_algorithm/firefly.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/kernel/pyslvs_algorithm/planarlinkage.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/kernel/pyslvs_algorithm/rga.$(CPPYTHON)-win_amd64.pyd;." \
--add-binary="core/kernel/pyslvs_algorithm/tinycadlib.$(CPPYTHON)-win_amd64.pyd;."
	rename .\dist\launch_pyslvs.exe pyslvs.exe
else
	$(eval PYTHON = py$(shell python3 -c "import sys;t='{v[0]}{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"))
	$(eval PYQTPATH = $(shell python3 -c "import PyQt5, os, sys;sys.stdout.write(os.path.dirname(PyQt5.__file__))"))
	@echo --Python Version $(PYTHON)--
	pyinstaller -F $< --exclude-module="PyQt4"
	mv dist/launch_pyslvs dist/pyslvs
endif
	@echo ---Done---

run: build dist
ifeq ($(OS),Windows_NT)
	@dist/pyslvs.exe -h
else
	@dist/pyslvs -h
endif

DEBIANCONTROL = dist/temp/DEBIAN/control
deb: build dist/pyslvs
ifeq ($(OS),Windows_NT)
	@echo ---Ubuntu only---
else
	mkdir dist/temp dist/temp/DEBIAN dist/temp/usr/ dist/temp/usr/bin dist/temp/usr/share/
	touch $(DEBIANCONTROL)
	echo 'Package: pyslvs' >> $(DEBIANCONTROL)
	$(eval PYSLVS = "Version: $(shell python3 -c "import sys;from core.info.info import VERSION;sys.stdout.write('{}.{}.{}'.format(*VERSION[:-1]))")")
	echo $(PYSLVS) >> $(DEBIANCONTROL)
	echo 'Architecture: all' >> $(DEBIANCONTROL)
	echo 'Description: Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.' >> $(DEBIANCONTROL)
	echo 'Maintainer: Yuan Chang <daan0014119@gmail.com>' >> $(DEBIANCONTROL)
	mv dist/pyslvs dist/temp/usr/share/
	ln -s /usr/share/pyslvs dist/temp/usr/bin/pyslvs
	mv dist/temp dist/pyslvs
	dpkg -b dist/pyslvs
endif
	@echo ---Done---

clean:
ifeq ($(OS),Windows_NT)
	-rd build /s /q
	-rd dist /s /q
	-del launch_pyslvs.spec
else
	-rm -f -r build
	-rm -f -r dist
	-rm -f launch_pyslvs.spec
endif

clean-kernel:
	$(MAKE) -C core/kernel/pyslvs_algorithm clean
	$(MAKE) -C core/kernel/python_solvespace clean

clean-all: clean-kernel clean
