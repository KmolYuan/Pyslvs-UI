# Command Set

The followings are the commands of handling Pyslvs-UI repository.
If you just want to try the last nightly version, just follow the steps of [full installation](#full-installation).

Pyslvs-UI and its kernel are the [PEP 517](https://www.python.org/dev/peps/pep-0517) Python project,
which requires some tools as shown below.

| Tool | Description |
|:----:|:-----------:|
| pip & setuptools | Must upgrade to the new version to support PEP 517. |
| wheel | Supports wheel functions. |
| build | Used to build the wheels and source distributions under PEP 517. |
| apimd | Used to generate the documentation. |
| PyInstaller | Used to make standalone distributions. |

Users of Windows platform must be able to execute shell scripts.
(Msys2 is recommended)

## Full Installation

```bash
pip install -e .
```

To update developing kernel only,
goto `pyslvs` repository and execute the same command again.

## Python Package Distribution

Use `pip` only: (only supports wheels)

```bash
pip wheel . --no-deps -w dist
```

Use `build`: (both wheels and sources)

```bash
python -m build
python -m build --wheel
python -m build --sdist
```

## Standalone Distribution

Use PyInstaller: (Windows and macOS)

```bash
./scripts/pyinstaller_recipe.sh
```

Use AppImage: (Linux)

```bash
./scripts/appimage_recipe.sh
```

## Documentation Generation

```bash
./scripts/gen_doc.sh
```

## Qt Resources Generation

```bash
python scripts/compile_resource.py --ui
python scripts/compile_resource.py --qrc
```

## Uninstallation

```bash
pip uninstall pyslvs-ui pyslvs
```

Extras:

```bash
pip uninstall python-solvespace
```
