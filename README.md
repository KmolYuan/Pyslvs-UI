Pyslvs(PySolveSpace)
===

![](icons/title.png)

A GUI-based tool solving 2D linkage subject.

+ **Planar Linkages Simulation**: Kernel from Solvespace Python bundle.

+ **Dimensional Synthesis**: Kernel from three Cython algorithm API.

Compatible with Python 3.4, PyQt 5.5 and above.

Cross-platform Development: Ubuntu and Windows OS

![](icons/cover/main.png)

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

Symbolic
---

1. Point

    ![](icons/cover/Point.png)

1. Line (Link)

    ![](icons/cover/Line.png)

1. Chain (Stay Chain)

    ![](icons/cover/Chain.png)

1. Shaft (Drive Shaft)

    ![](icons/cover/Shaft.png)

1. Slider

    ![](icons/cover/Slider.png)

1. Rod (Piston)

    ![](icons/cover/Rod.png)

Path Track
---

![](icons/cover/PathTrack.png)

Calculate the path of the node.

![](icons/cover/PathTrack_all.png)

View them in the table.

![](icons/cover/PathResult.png)

Triangle Solver
---

![](icons/cover/TriangleSolver.png)

Triangle solver find the node position by using three triangular relationship.

![](icons/cover/TriangleSolver_merge.png)

Then merge into canvace as well.

Algorithm
---

![](icons/cover/Algorithm.png)

Contains three algorithms:

+ Genetic Algorithm
+ Firefly Algorithm
+ Differential Evolution

Specify a path and options to generate a crank rocker.

Requirement
===

You should install some python module first.

Linux:

```bash
$sudo pip3 install -r requirements.txt
```

Windows:

```bash
>pip install -r requirements.txt
```

Compile
===

Make sure computer is installed [Qt5] and [PyQt5] in the same version.

After following operation, the executable file's folder is located at `dist` / `launch_pyslvs` folder.

As your wish, it can be renamed or moved out and operate independently in no-Python environment.

Linux
---

Use PyInstaller or cxFreeze as you like.

First, enter the storage folder.

```bash
$sudo pip3 install PyInstaller
$make
```

Windows
---

Python 3: [Anaconda] for Windows 64 bit.

Use both PyInstaller and cxFreeze to build.

Other require installation: [MinGW] for win64.

First, enter the storage folder.

```bash
>pip install cx_Freeze PyInstaller
>make
```

If you installed PyInstaller with problem of coding error, you can try another source:

```bash
>pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
```

Power By
===

Made by PyQt 5.7 and Python editor [Eric 6].

Including Python module: [PyQt5], [peewee], [dxfwrite]

Here is the **origin kernel** repository:

* [Python-solvespace]

* [Dimensional Synthesis of Planar Four-bar Linkages]

* [Triangle solver]

Build Kernel
===

Compiled kernel is in the `core` folder.

* Linux (64 bit): Python 3.4, Python 3.5

* Windows (64 bit): Python 3.5, Python 3.6

If your Python version or platform is not compatible, maybe you should build them by self.

```bash
git submodule init
git submodule update
```

Then follow the instructions in the readme.

[PyQt5]: http://doc.qt.io/qt-5/index.html
[Qt5]: https://www.qt.io/download/
[Anaconda]: https://www.continuum.io/downloads
[MinGW]: https://sourceforge.net/projects/mingw-w64/files/latest/download?source=files
[Eric 6]: http://eric-ide.python-projects.org/
[peewee]: http://docs.peewee-orm.com/en/latest/
[dxfwrite]: https://pypi.python.org/pypi/dxfwrite/

[Python-solvespace]: https://github.com/KmolYuan/python-solvespace
[Dimensional Synthesis of Planar Four-bar Linkages]: https://github.com/kmollee/algorithm
[Triangle solver]: https://gist.github.com/KmolYuan/c5a94b769bc410524bba66acc5204a8f
