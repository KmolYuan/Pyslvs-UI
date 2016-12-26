@echo off

echo ---Pyslvs Windows Build---

rd .\build /s /q
rd .\dist /s /q

pyinstaller -w launch_pyslvs.py -i .\icons\main_big.ico
python setup.py build

echo ---Copying Folder and Files---

xcopy .\build\launch_pyslvs .\build\exe.win-amd64-3.5 /s /y
rd .\dist /s /q
rd .\build\launch_pyslvs /s /q
del .\launch_pyslvs.spec

echo ---Done---

.\build\exe.win-amd64-3.5\launch_pyslvs.exe
