@echo off

echo ---Pyslvs Windows Build---

rd .\build /s /q
rd .\dist /s /q

REM Temporarily display log for debugging.
pyinstaller launch_pyslvs.py -i .\icons\main_big.ico
python setup.py build

echo ---Copying Folder and Files---

xcopy .\build\exe.win-amd64-3.5\core .\dist\launch_pyslvs\core\ /s /y /i
rd .\build /s /q
del .\launch_pyslvs.spec

echo ---Done---

.\dist\launch_pyslvs\launch_pyslvs.exe
