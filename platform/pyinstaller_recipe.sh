#!/usr/bin/env bash
# Build executable with PyInstaller

APP=Pyslvs

########################################################################
# Create a virtual environment
########################################################################

REPODIR=$(readlink -f "$(dirname "$(readlink -f "${0}")")/..")
cd "${REPODIR}" || exit

# Run virtualenv
pip install virtualenv || exit
python -m virtualenv ENV --always-copy --verbose
source ENV/bin/activate

# Show python and pip versions
python --version
python -m pip --version

# Install python dependencies
python -m pip install -r requirements.txt || exit
cd "${REPODIR}/pyslvs" || exit
python setup.py install && python tests
cd "${REPODIR}" || exit

########################################################################
# Pack executable
########################################################################

PYSLVSVER=$(python -c "from pyslvs import __version__;print(__version__)")
COMPILERVER=$(python -c "import platform;print(''.join(platform.python_compiler().split()[:2]).replace('.', '').lower())")
SYSVER=$(python -c "import platform;print(platform.machine().lower())")
EXENAME=pyslvs-${PYSLVSVER}.${COMPILERVER}-${SYSVER}
if [[ "$(uname)" == "Darwin" ]]; then
  FLAG=-w
  ICON=icns
else
  FLAG=
  ICON=ico
fi

# Run PyInstaller
python -m pip install https://github.com/pyinstaller/pyinstaller/tarball/develop || exit
python -m PyInstaller ${FLAG} -F launch_pyslvs.py -i pyslvs_ui/icons/main.${ICON} -n ${APP}
cd "${REPODIR}/dist" || exit
if [[ "$(uname)" == "Darwin" ]]; then
  mv ${APP} "${EXENAME}.run"
  mv ${APP}.app "${EXENAME}.app"
  zip -r "${EXENAME}.app.zip" "${EXENAME}.app"
else
  mv ${APP}.exe "${EXENAME}.exe"
  7z a -tzip "${EXENAME}.zip" "${EXENAME}.exe"
fi
