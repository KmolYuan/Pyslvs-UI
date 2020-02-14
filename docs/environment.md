# Environment

## Architecture

Pyslvs is a Graphical User Interface (GUI) program written in Python.
After installed Python launcher on your platform,
the programming script can be compiled as an executable file.

In development state, Pyslvs including several dynamic libraries,
which are need to be compiled first.

## Dependencies

The actual test and deployment platforms on CI/CD service:

| Platforms (64-bit) | Windows | macOS | Ubuntu |
|:------------------:|:-------:|:-----:|:------:|
| Service | [AppVeyor][ci1] | [Travis][ci2] | [Travis][ci3] |
| OS version | Windows Server 2019 | Xcode 10.0 (10.13) | Xenial (16.04) |
| Python 3.7 | O | O | O |
| Python 3.8 | $\Delta$ (not support MinGW) | O | O |

**Please note that the other platforms may be available but I have not tested before.**

[ci1]: https://www.appveyor.com/docs/windows-images-software/
[ci2]: https://docs.travis-ci.com/user/reference/osx/
[ci3]: https://docs.travis-ci.com/user/reference/linux/

Install dependencies:

```bash
pip install -r requirements.txt
```

### Ubuntu and macOS

It is recommended to use [pyenv](https://github.com/pyenv/pyenv),
which will be more easier to handle Python version instead of using system Python.
So any operation about Python will not required `sudo` or `--user` option.

```bash
# Install supported version of Pyslvs
# The devlopment tools need to prepare first (like openssl, sqlite3)
pyenv install --list  # show all available versions
pyenv install 3.7.4
pyenv global 3.7.4
python --version  # Python 3.7.4
pip --version  # pip 19.2.2 from /home/user/.pyenv/versions/3.7.4/lib/python3.7/site-packages/pip (python 3.7)
```

### Windows

Python 3: [Official Python] for Windows 64 bit.

Makefile tool: MinGW or Msys 2.

#### Msys 2

Use [Msys 2](http://www.msys2.org/) and [MinGW 64-bit](https://sourceforge.net/projects/mingw-w64/),
they also can be installed by Windows package manager [Chocolatey](https://chocolatey.org/).

```batch
choco install msys2
```

When you are using Msys2, following command might be helpful:

```bash
# Install tools for Msys.
# Open the "mingw64.exe" shell.

# Install MinGW
pacman -S mingw-w64-x86_64-gcc
# Install Make
pacman -S mingw-w64-x86_64-make
# The "make" command is named as "mingw32-make". You can rename it by:
mv /mingw64/bin/mingw32-make /mingw64/bin/make

# Install patch
pacman -S patch
```

And the programs should be added in to environment variable (with administrator).

```batch
setx Path "C:\tools\msys64\usr\bin;%Path%" /M
```

Setup Python compiler as GCC / G++ of MinGW64:

```batch
platform\set_pycompiler C:\Python37 mingw32
```

And it will be useful if Make tool in Msys can't find Windows command (such like `copy`, `rd` or `del`):

```makefile
ifeq ($(OS),Windows_NT)
    # Rewrite "SHELL" variable.
    SHELL = cmd
endif
```

#### Visual C++

Install from [official website](https://visualstudio.microsoft.com/downloads)

And setup Python compiler:

```batch
platform\set_pycompiler C:\Python37 msvc
```

### Qt Designer (Development)

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

### Fcitx QIMPanel Plugins on Linux

The Fcitx input method support is depanded on the plugins of PyQt.
Copy the libraries from `/usr/lib/x86_64-linux-gnu/qt5/plugins/` into `python/site-packages/PyQt5/Qt/plugins/`.

The plugins is `platforminputcontexts/libfcitxplatforminputcontextplugin.so`.

!!! warning
    Please note that some PyQt plugins are version depended,
    so the AppImage distributions are exclude these supports.

## Kernels Requirement

About the development tools, please see [Dependencies](#dependencies).

Make command:

```bash
make
```

This project including two kernels should build.

!!! note
    The kernels can also be installed from pip with specified version.
    The Makefile command will build them from source.

### Pyslvs Kernel

[Pyslvs]: Core libraries of this project.
The version should be same as Pyslvs-UI.

Install it by `pip install pyslvs==xx.xx` to specify the version.
Or just build from the submodule.

### Python-Solvespace Kernel

[Python-Solvespace]: Python bundle of [Solvespace] library.

Install it by `pip install python-solvespace`.

## Stand-alone Executable File

As your wish, it can be renamed or moved out and operate independently in no-Python environment.

Make command:

```bash
make pack
```

### Ubuntu

Use shell command to build as [AppImage].
Because of it is more suitable with PyQt module than [PyInstaller].

After following operation, the executable file is in a folder named `out`.
The script also install `virtualenv` automatically if no executable command.

!!! warning
    Check the `glibc` version from `ldd --version`,
    it must be equal or higher than package's.

### Windows and macOS

Use [PyInstaller] with `virtualenv`, they will install automatically if no executable command.

After following operation, the executable file is in a folder named `dist`.

!!! note
    The Windows platform version requirement is same as the Python that packed.

On macOS, PyInstaller will generate two executable files (refer [here](https://pyinstaller.readthedocs.io/en/stable/usage.html#building-mac-os-x-app-bundles)).

```bash
# Run Unix-like executable file.
# Can not run it directly in Finder.
./executable --use-arguments-here

# Run macOS app file. (Can not use any arguments)
# Same as double click it in Finder.
open ./executable.app
```

!!! warning
    The version of macOS must be equal or higher than executable's.

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

[PyInstaller]: https://www.pyinstaller.org/
[Solvespace]: http://solvespace.com
[Qt5]: https://www.qt.io/download/

[Official Python]: https://www.python.org/
[AppImage]: http://appimage.org

[Python-Solvespace]: https://github.com/KmolYuan/solvespace/tree/python
[Pyslvs]: https://github.com/KmolYuan/pyslvs
