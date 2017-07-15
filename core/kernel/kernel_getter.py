# -*- coding: utf-8 -*-
#System infomation
import sys, platform
py_nm = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
py_nm += 'w' if platform.system().lower()=='windows' else ''
#SLVS Version & pyslvs_generate Version
if py_nm=='36w':
    from .py36w.slvs import *
elif py_nm=='35w':
    from .py35w.slvs import *
elif py_nm=='35':
    from .py35.slvs import *
elif py_nm=='34':
    from .py34.slvs import *
from .pyslvs_generate import tinycadlib
from .pyslvs_generate.planarlinkage import build_planar
from .pyslvs_generate.rga import Genetic
from .pyslvs_generate.firefly import Firefly
from .pyslvs_generate.de import DiffertialEvolution
