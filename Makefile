all: build run

BUILDFLAG = --path=./core/kernel/py35/ --path=./core/kernel/pyslvs_generate/py35/

#Windows: Temporarily display log for debugging.
build: launch_pyslvs.py
	@echo ---Pyslvs  Build---
ifeq ($(OS),Windows_NT)
	@echo ---Windows Version---
	pyinstaller launch_pyslvs.py $(BUILDFLAG) -i ./icons/main_big.ico
	python setup.py build
	@echo ---Copying Folder and Files---
	xcopy .\build\exe.win-amd64-3.6\core\kernel\py36w .\dist\launch_pyslvs\core\kernel\py36w /s /y /i
	xcopy .\build\exe.win-amd64-3.6\core\kernel\pyslvs_generate\py36w .\dist\launch_pyslvs\core\kernel\pyslvs_generate\py36w /s /y /i
	rename .\dist\launch_pyslvs Pyslvs
else
	@echo ---Linux Version---
	pyinstaller launch_pyslvs.py $(BUILDFLAG)
	mv dist/launch_pyslvs dist/Pyslvs
endif
	@echo ---Done---

run: build dist/Pyslvs
ifeq ($(OS),Windows_NT)
	@dist/Pyslvs/launch_pyslvs.exe
else
	@dist/Pyslvs/launch_pyslvs
endif

DEBIANCONTROL = dist/temp/DEBIAN/control

deb: build dist/Pyslvs
ifeq ($(OS),Windows_NT)
	@echo ---Ubuntu only---
else
	mkdir dist/temp dist/temp/DEBIAN dist/temp/usr/ dist/temp/usr/bin dist/temp/usr/share/
	touch $(DEBIANCONTROL)
	echo 'Package: pyslvs' >> $(DEBIANCONTROL)
	echo 'Version: 0.6.4' >> $(DEBIANCONTROL)
	echo 'Architecture: all' >> $(DEBIANCONTROL)
	echo 'Description: Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.' >> $(DEBIANCONTROL)
	echo 'Maintainer: Yuan Chang <daan0014119@gmail.com>' >> $(DEBIANCONTROL)
	mv dist/Pyslvs dist/temp/usr/share/
	ln -s /usr/share/Pyslvs/launch_pyslvs dist/temp/usr/bin/pyslvs
	mv dist/temp dist/Pyslvs
	dpkg -b dist/Pyslvs
endif

clean:
ifeq ($(OS),Windows_NT)
	rd build /s /q
	rd dist /s /q
	del launch_pyslvs.spec
else
	rm -f -r build
	rm -f -r dist
	rm -f launch_pyslvs.spec
endif
