# Command Set

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
