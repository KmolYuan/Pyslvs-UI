#!/usr/bin/env bash
# Setup for UX like shell

# Usage: sh set_pycompiler.sh /c/Python37 mingw32
# Where ${PYTHON_DIR} is the directory of your Python installation.
# Compiler option can be "mingw32" or "msvc".
# In Pyslvs project.
HERE=$(readlink -f "$(dirname "$(readlink -f "${0}")")")
cd "${HERE}" || exit
PYTHON_DIR=$1
COMPILER=$2

# Create "distutils.cfg"
DISTUTILS=${PYTHON_DIR}/Lib/distutils/distutils.cfg
[ -f "${DISTUTILS}" ] && rm "${DISTUTILS}"
cat >"${DISTUTILS}" <<EOF
[build]
compiler=${COMPILER}
EOF
echo patched file "${DISTUTILS}"
# Apply the patch of "cygwinccompiler.py".
# Unix "patch" command of Msys.
patch -N "${PYTHON_DIR}/lib/distutils/cygwinccompiler.py" "${HERE}/cygwinccompiler.diff"
patch -N "${PYTHON_DIR}/include/pyconfig.h" "${HERE}/pyconfig.diff"

# Copy "vcruntime140.dll" to "libs".
cp "${PYTHON_DIR}/vcruntime140.dll" "${PYTHON_DIR}/libs"
echo copied "vcruntime140.dll".
