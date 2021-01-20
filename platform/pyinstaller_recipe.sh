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
python -m pip install -e .
cd "${REPODIR}" || exit

########################################################################
# Pack executable
########################################################################

PYSLVSVER=$(python -c "from pyslvs_ui import __version__;print(__version__)")
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

cat >"${REPODIR}/hook.py" <<EOF
# -*- coding: utf-8 -*-
from pyslvs_ui.__main__ import main
main()
EOF

# Run PyInstaller
python -m pip install https://github.com/pyinstaller/pyinstaller/tarball/develop || exit
python -m PyInstaller ${FLAG} -F hook.py -i pyslvs_ui/icons/main.${ICON} -n ${APP}
rm -f "${REPODIR}/hook.py"
cd "${REPODIR}/dist" || exit
if [[ "$(uname)" == "Darwin" ]]; then
  mv ${APP} "${EXENAME}.run"
  mv ${APP}.app "${EXENAME}.app"
  "${EXENAME}.run" test
  zip -r "${EXENAME}.app.zip" "${EXENAME}.app"
else
  mv ${APP}.exe "${EXENAME}.exe"
  "${EXENAME}.exe" test
  7z a -tzip "${EXENAME}.zip" "${EXENAME}.exe"
fi
