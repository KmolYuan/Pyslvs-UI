@echo off

echo ---Pyslvs Windows Build---

rd .\build /s /q
rd .\dist /s /q

pyinstaller -w launch_pyslvs.py -i .\icons\main.ico
python setup.py build

xcopy .\build\launch_pyslvs .\build\exe.win-amd64-3.5 /s /y

echo ---Done---

.\build\exe.win-amd64-3.5\launch_pyslvs.exe
