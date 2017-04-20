# -*- coding: utf-8 -*-
#System infomation
import sys, platform
py_nm = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
py_nm += 'w' if platform.system().lower()=='windows' else ''
