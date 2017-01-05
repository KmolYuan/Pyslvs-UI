Pyslvs(PySolveSpace)
===

![](icons/title.png)

A GUI-based tool solving 2D linkage subject.

Compatible with Python 3.4 and above.

![](icons/cover.png)

How to startup
---

Open GUI by Python:

```bash
$python3 launch_pyslvs.py
```

Or see help:

```bash
$python3 launch_pyslvs.py --help
```

Compile
===

Linux & Mac
---

Use PyInstaller or cxFreeze as you like.

First, enter the storage folder.

```bash
$sudo pip3 install PyInstaller
$make
```

Windows
---

Use both PyInstaller and cxFreeze to build.

Recommended installation: [MinGW](https://sourceforge.net/projects/mingw-w64/files/latest/download?source=files) for win64.

First, enter the storage folder.

```bash
>pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
>pip install cx_Freeze
>make
```

And than, the executable folder is located at `\build`, called `\exe.win-amd64-3.5`.

As your wish, it can be renamed or moved out and operate independently in no-Python environment.

Collaboration
===

The manual is being written, you can see [here](https://github.com/40323230/Pyslvs-manual/).

Power By
===

Made by PyQt 5.7 and Python editor [Eric 6](http://eric-ide.python-projects.org/).

Including Python module: [PyQt5](http://doc.qt.io/qt-5/index.html), [peewee](http://docs.peewee-orm.com/en/latest/), [dxfwrite](https://pypi.python.org/pypi/dxfwrite/)

Here is **origin kernel** repository:

* [https://github.com/40323230/python-solvespace](https://github.com/40323230/python-solvespace)

* [https://github.com/kmollee/django-project-template](https://github.com/kmollee/django-project-template)
