# Environment

## Architecture

Pyslvs is a Graphical User Interface (GUI) program written in Python.
After installed Python launcher on your platform,
the programming script can be compiled as an executable file.

In development state, Pyslvs including several dynamic libraries,
which are need to be compiled first.

## Dependencies

Actual testing platforms with CI:

| Platform (64-bit) | Windows | MacOS | Ubuntu |
|:------------------:|:-------:|:-----:|:------:|
| Python 3.7 | O | O | O |

**Please note that the other platforms may be available but I have not tested before.**

Install dependences:

```bash
pip install -r requirements.txt
```

**Mac OS and Ubuntu**:

It is recommended to use [pyenv](https://github.com/pyenv/pyenv),
which will be more easier to handle Python version instead of using system Python.
So any operation about Python will not required `sudo` or `--user` option.

```bash
# Install supported version of Pyslvs
# The devlopment tools need to prepare first (like openssl, sqlite3)
pyenv install --list  # show all available versions
pyenv install 3.7.4
pyenv install 3.7-dev
pyenv global 3.7.4
python --version  # Python 3.7.4
pip --version  # pip 19.2.2 from /home/user/.pyenv/versions/3.7.4/lib/python3.7/site-packages/pip (python 3.7)
```

**Windows**:

Python 3: [Official Python] for Windows 64 bit.

Makefile tool: [MinGW] or [Msys 2][msys].

### Qt Stuff (Development)

PyQt5 and its additional modules are now packed into the wheel file that most of platform can install them directly.

You need to get original Qt tools for development, which can be used to design the *.ui files,
they are not the requirement if you just want to run Pyslvs.

Download and install [Qt5] to get the tools.

**Ubuntu**:

Ubuntu users can obtain them via APT:

```bash
sudo apt install qttools5-dev-tools
```

**Windows**:

Windows user can get Qt tools by pip (maybe not newest version), without to install Qt package.

```bash
pip install pyqt5-tools
```

## Kernels Requirement

About the development tools, please see [Dependencies](#dependencies).

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

# Install GCC
pacman -S mingw-w64-x86_64-gcc
# Install Make
pacman -S mingw-w64-x86_64-toolchain
# A list of tools will shown, choose 13 ("mingw-w64-x86_64-make").
# The "make" command is named as "mingw32-make". You can rename it:
mv /mingw64/bin/mingw32-make /mingw64/bin/make

# Install patch
pacman -S patch
```

And the programs should be added in to environment variable (with administrator).

```batch
setx Path %Path%C:\tools\msys64\mingw64\bin;C:\tools\msys64\usr\bin; /M
```

Setup Python compiler as gcc / g++ of MinGW64:

```batch
REM Where %PYTHON_DIR% is the directory of your Python installation.
REM In Pyslvs project.
set PYTHON_DIR=C:\Python37

REM Create "distutils.cfg"
echo [build]>> %PYTHON_DIR%\Lib\distutils\distutils.cfg
echo compiler = mingw32>> %PYTHON_DIR%\Lib\distutils\distutils.cfg

REM Apply the patch of "cygwinccompiler.py".
REM Unix "patch" command of Msys.
patch %PYTHON_DIR%\lib\distutils\cygwinccompiler.py platform\patch.diff

REM Copy "vcruntime140.dll" to "libs".
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
pip install virtualenv
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
