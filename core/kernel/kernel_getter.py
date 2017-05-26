# -*- coding: utf-8 -*-
#System infomation
import sys, platform
py_nm = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
py_nm += 'w' if platform.system().lower()=='windows' else ''
#SLVS Version & pyslvs_generate Version
if py_nm=='36w':
    from .py36w.slvs import *
    from .pyslvs_generate.py36w import tinycadlib
    from .pyslvs_generate.py36w.planarlinkage import build_planar
    from .pyslvs_generate.py36w.rga import Genetic
    from .pyslvs_generate.py36w.firefly import Firefly
    from .pyslvs_generate.py36w.de import DiffertialEvolution
elif py_nm=='35w':
    from .py35w.slvs import *
    from .pyslvs_generate.py35w import tinycadlib
    from .pyslvs_generate.py35w.planarlinkage import build_planar
    from .pyslvs_generate.py35w.rga import Genetic
    from .pyslvs_generate.py35w.firefly import Firefly
    from .pyslvs_generate.py35w.de import DiffertialEvolution
elif py_nm=='35':
    from .py35.slvs import *
    from .pyslvs_generate.py35 import tinycadlib
    from .pyslvs_generate.py35.planarlinkage import build_planar
    from .pyslvs_generate.py35.rga import Genetic
    from .pyslvs_generate.py35.firefly import Firefly
    from .pyslvs_generate.py35.de import DiffertialEvolution
elif py_nm=='34':
    from .py34.slvs import *
    from .pyslvs_generate.py34 import tinycadlib
    from .pyslvs_generate.py34.planarlinkage import build_planar
    from .pyslvs_generate.py34.rga import Genetic
    from .pyslvs_generate.py34.firefly import Firefly
    from .pyslvs_generate.py34.de import DiffertialEvolution
