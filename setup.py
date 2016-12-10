from cx_Freeze import setup, Executable
import sys
 
build_exe_options = {"packages": ["os"], "includes": ["PyQt5"], "excludes": ["tkinter"]}
 
base = None
if sys.platform == "win32":
    base = "Win32GUI"
 
setup(
    name = 'solvespack',
    version = '1',
    description = '.',
    executables=[Executable('launch_pyslvs.py', base=base)],
    options={"build_exe":build_exe_options},
)
