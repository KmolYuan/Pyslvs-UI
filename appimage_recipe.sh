#!/usr/bin/env bash
# This is a very simple example on how to bundle a Python application as an AppImage
# using virtualenv and AppImageKit using Ubuntu
# NOTE: Please test the resulting AppImage on your target systems and copy in any additional
# libraries and/or dependencies that might be missing on your target system(s).

########################################################################
# Create the AppDir
########################################################################

APP=pyslvs
LOWERAPP=${APP,,}

BASEDIR=$(dirname "$(readlink -f "${0}")")
cd ${BASEDIR} || exit
ENV=${BASEDIR}/ENV
APPDIR=${ENV}/${APP}.AppDir

mkdir -p ${APPDIR}

# Source some helper functions
wget -q https://raw.githubusercontent.com/AppImage/pkg2appimage/master/functions.sh -O ${ENV}/functions.sh
# shellcheck disable=SC1090
. ${ENV}/functions.sh

########################################################################
# Create a virtualenv inside the AppDir
########################################################################

cd ${APPDIR} && mkdir -p usr/bin
virtualenv ./usr --python=python3 --always-copy --verbose
source usr/bin/activate

# Show python and pip versions
python --version
pip --version

# Install python dependencies into the virtualenv
pip install -r ${BASEDIR}/requirements.txt
cd ${BASEDIR}/depend/pyslvs && python setup.py install && python tests
cd ${BASEDIR}/depend/solvespace/cython && python setup.py install && python tests
cd ${APPDIR} || exit

# Copy all built-in scripts
PYVER=$(python -c "from distutils import sysconfig;print(sysconfig.get_config_var('VERSION'))")
PYDIR=$(python -c "from distutils import sysconfig;print(sysconfig.get_config_var('DESTLIB'))")
MY_PYDIR=${APPDIR}/usr/lib/python${PYVER}

echo "Remove venv distutils ..."
rm -fr ${MY_PYDIR}/distutils

echo "Copy builtin scripts from '${PYDIR}' to '${MY_PYDIR}' ..."
cd ${PYDIR} || exit
for p in "*.py" "*.so"; do
  find . -name "${p}" -exec install -v -D {} ${MY_PYDIR}/{} \;
done

cd ${MY_PYDIR} || exit
for d in "test" "venv" "idlelib"; do
  rm -fr ${d}
done

# Python libraries
cd ${APPDIR} || exit
cp -n -v "$(python -c "from distutils import sysconfig;print(sysconfig.get_config_var('SCRIPTDIR'))")"/libpython3*.so* usr/lib

deactivate

########################################################################
# "Install" app in the AppDir
########################################################################

# Make launch script
cp ${BASEDIR}/launch_pyslvs.py usr/bin/${LOWERAPP}
sed -i "1i\#!/usr/bin/env python3" usr/bin/${LOWERAPP}
chmod a+x usr/bin/${LOWERAPP}

cp ${BASEDIR}/icons_rc.py usr/bin
cp ${BASEDIR}/preview_rc.py usr/bin
cd ${BASEDIR}/core || exit
find . -name "*.py" -exec install -v -D {} ${APPDIR}/usr/bin/core/{} \;

########################################################################
# Finalize the AppDir
########################################################################

cd ${APPDIR} || exit
get_apprun

cd ${BASEDIR} || exit
VERSION=$(python3 -c "from pyslvs import __version__; print(__version__)")
echo "${VERSION}"
cd ${APPDIR} || exit

cat >${LOWERAPP}.desktop <<EOF
[Desktop Entry]
Name=${APP}
Exec=${LOWERAPP}
Type=Application
Categories=Development;Education;
Icon=${LOWERAPP}
StartupNotify=true
Comment=Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
EOF

# Make the AppImage ask to "install" itself into the menu
get_desktopintegration ${LOWERAPP}
cp ${BASEDIR}/icons/main.png ${LOWERAPP}.png

########################################################################
# Bundle dependencies
########################################################################

copy_deps
copy_deps
copy_deps
delete_blacklisted
move_lib

rm -fr ./opt ./usr/share

########################################################################
# Package the AppDir as an AppImage
########################################################################

cd ${ENV} || exit
generate_type2_appimage
