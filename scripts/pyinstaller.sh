#!/usr/bin/env bash
# Build executable with PyInstaller

APP=Pyslvs

########################################################################
# Create a virtual environment
########################################################################

REPODIR=$(readlink -f "$(dirname "$(readlink -f "${0}")")/..")
cd "${REPODIR}" || exit

# Run virtualenv
python -m venv ENV --copies
if [[ "$(uname)" == "Darwin" ]]; then
  source ENV/bin/activate
else
  source ENV/Scripts/activate
fi

# Show python and pip versions
python --version
python -m pip --version

# Install python dependencies
python -m pip install .

########################################################################
# Pack executable
########################################################################

PYSLVSVER=$(python -c "from pyslvs_ui import __version__;print(__version__)")
COMPILERVER=$(python -c "import platform;print(''.join(platform.python_compiler().split()[:2]).replace('.', '').lower())")
SYSVER=$(python -c "import platform;print(platform.machine().lower())")
EXENAME=pyslvs-${PYSLVSVER}.${COMPILERVER}-${SYSVER}
if [[ "$(uname)" == "Darwin" ]]; then
  CONSOLE=-w
  ICON=icns
  ICON_PATH="pyslvs_ui/icons/*:pyslvs_ui/icons"
else
  CONSOLE=-c
  ICON=ico
  ICON_PATH="pyslvs_ui/icons/*;pyslvs_ui/icons"
fi

# Run PyInstaller
python -m pip install https://github.com/pyinstaller/pyinstaller/tarball/develop || exit
python -m PyInstaller ${CONSOLE} -F "${REPODIR}/scripts/entry.py" -n ${APP} \
  -i "pyslvs_ui/icons/main.${ICON}" \
  --add-data ${ICON_PATH} \
  --additional-hooks-dir "${REPODIR}/scripts"
cd "${REPODIR}/dist" || exit
if [[ "$(uname)" == "Darwin" ]]; then
  ls -A -1
  mv ${APP} "${EXENAME}.run"
  mv ${APP}.app "${EXENAME}.app"
  "${EXENAME}.run" test
  zip -r "${EXENAME}.app.zip" "${EXENAME}.app"
else
  mv ${APP}.exe "${EXENAME}.exe"
  "${EXENAME}.exe" test
  7z a -tzip "${EXENAME}.zip" "${EXENAME}.exe"
fi
