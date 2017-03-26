all: build run

#Windows: Temporarily display log for debugging.
build: launch_pyslvs.py
	@echo ---Pyslvs  Build---
ifeq ($(OS),Windows_NT)
	@echo ---Windows Version---
	pyinstaller launch_pyslvs.py -i ./icons/main_big.ico
	python setup.py build
	@echo ---Copying Folder and Files---
	xcopy .\build\exe.win-amd64-3.5\core\kernel\py35w .\dist\launch_pyslvs\core\kernel\py35w /s /y /i
	xcopy .\build\exe.win-amd64-3.5\core\kernel\pyslvs_generate\py35w .\dist\launch_pyslvs\core\kernel\pyslvs_generate\py35w /s /y /i
else
	@echo ---Linux Version---
	pyinstaller launch_pyslvs.py
endif
	@echo ---Done---

run: build
ifeq ($(OS),Windows_NT)
	@dist/launch_pyslvs/launch_pyslvs.exe
else
	@dist/launch_pyslvs/launch_pyslvs
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
