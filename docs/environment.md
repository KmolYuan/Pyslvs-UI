# Environment

## Architecture

Pyslvs is a Graphical User Interface (GUI) program written in Python.
After installed Python launcher on your platform,
the programming script can be compiled as an executable file.

In development state, Pyslvs including several dynamic libraries,
which are need to be compiled first.

## Dependency

Actual testing platforms with CI:

+ ![w3.7](https://img.shields.io/badge/Windows%20x64-Python%203.7-blue.svg)
+ ![m3.7](https://img.shields.io/badge/macOS%20Sierra-Python%203.7-ff69b4.svg)
+ ![u3.7](https://img.shields.io/badge/Ubuntu%20x64-Python%203.7-orange.svg)

**Please note that the other platforms may be available but I have not tested before.**

**Mac OS and Ubuntu**:

```bash
# Local Python
pip3 install -r requirements.txt

# Global Python
sudo pip3 install -r requirements.txt
```

**Windows**:

Python 3: [Official Python] for Windows 64 bit.

Makefile tool: [MinGW] or [Msys 2][msys].

```bash
pip install -r requirements.txt
```

### PyQt Stuff (Development)

PyQt5 and QtChart are now pack into the wheel file that Windows and Ubuntu can install them directly.

Qt tools can be used to design the *.ui files, they are not the requirement if you just want to run Pyslvs.

**Mac OS and Ubuntu**:

Download and install [Qt5] to get the tools.

**Windows**:

Windows user can get Qt tools by pip (maybe not newest version), without to install Qt package.

```bash
pip install pyqt5-tools
```

## Kernels Requirement

About the development tools, please see [Modules Requirement](#modules-requirement).

Make command:

```bash
make build-kernel
```

This project including two kernels should build.

### Pyslvs Kernel

[Pyslvs]: Core libraries of this project.

Make command:

```bash
make build-pyslvs
```

#### Mac OS and Ubuntu

User can compile the kernel by [Cython](http://cython.org/) directly.

#### Windows

There's two options to choose SDK:

1. Using Microsoft Visual Studio. You can get it from [here][visualstudio-link], then startup the Visual Studio Community and install Windows SDK.
1. Using [Msys 2][msys]. It is based on MinGW 64-bit version.
1. Just using [MinGW 64-bit][mingw64].

[visualstudio-link]: https://www.visualstudio.com/downloads/
[msys]: http://www.msys2.org/
[mingw64]: https://sourceforge.net/projects/mingw-w64/

When using Msys2, following command might be helpful:

```bash
# Install tools for Msys.
# Open the "mingw64.exe" shell.
pacman -S mingw-w64-x86_64-gcc
pacman -S mingw-w64-x86_64-toolchain
# A list of tools will shown, choose "mingw-w64-x86_64-make".
# The "make" command is named as "mingw32-make".
pacman -S patch
```

Setup Python compiler as gcc / g++ of MinGW64:

```bash
# Where %PYTHON_DIR% is the directory of your Python installation.
# In Pyslvs project.

# Create "distutils.cfg"
echo [build]>> %PYTHON_DIR%\Lib\distutils\distutils.cfg
echo compiler = mingw32>> %PYTHON_DIR%\Lib\distutils\distutils.cfg

# Apply the patch of "cygwinccompiler.py".
# Unix "patch" command of Msys.
patch %PYTHON_DIR%\lib\distutils\cygwinccompiler.py platform\patch.diff

# Copy "vcruntime140.dll" to "libs".
copy %PYTHON_DIR%\vcruntime140.dll %PYTHON_DIR%\libs
```

And it will be useful if Make tool in Msys can't find Windows command (such like `copy`, `rd` or `del`):

```makefile
ifeq ($(OS),Windows_NT)
    # Rewrite "SHELL" variable.
    SHELL = cmd
endif
```

### Python-Solvespace Kernel

[Python-Solvespace]: Python bundle of [Solvespace] library.

Make command:

```bash
make build-solvespace
```

The compile steps of this kernel has same way as Pyslvs kernel.

### Stand-alone Executable File

As your wish, it can be renamed or moved out and operate independently in no-Python environment.

#### Ubuntu

Use shell command to build as [AppImage].

After following operation, the executable file is in `out` folder.

Make command:

```bash
sudo pip3 install virtualenv
make
```

#### Mac OS and Windows

Use PyInstaller to build.

After following operation, the executable file is in `dist` folder.

Make command:

```bash
pip install pyinstaller
make
```

On Mac OS, PyInstaller will generate two executable files (refer [here][pinstaller-mac]).

[pinstaller-mac]: https://pyinstaller.readthedocs.io/en/stable/usage.html#building-mac-os-x-app-bundles

```bash
# Run Unix-like executable file.
# Can not run it directly in Finder.
./executable --use-arguments-here

# Run Mac app file. (Can not use any arguments)
# Same as double click it in Finder.
open ./executable.app
```

## Documentation

This documentation is built by [MkDocs](https://www.mkdocs.org/).

If you want to demo the site in localhost, install MkDocs and the documentation requirements.

```bash
pip install mkdocs
pip install -r doc-requirements.txt
```

Start the local server:

```bash
mkdocs serve
```

The file `mkdocs.yml` and the contents of directory `docs` is a MkDocs project.
The markdown files are the resources of this site.

[Solvespace]: http://solvespace.com
[Qt5]: https://www.qt.io/download/

[Official Python]: https://www.python.org/
[MinGW]: https://sourceforge.net/projects/mingw-w64/files/

[AppImage]: https://github.com/AppImage/AppImages

[Python-Solvespace]: https://github.com/KmolYuan/solvespace/tree/python
[Pyslvs]: https://github.com/KmolYuan/pyslvs
