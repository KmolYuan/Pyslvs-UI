# -*- coding: utf-8 -*-
from .pyVersion import py_nm
#SLVS Version & pyslvs_generate Version
if py_nm=='36w':
    from .py36w.slvs import *
elif py_nm=='35w':
    from .py35w.slvs import *
elif py_nm=='35':
    from .py35.slvs import *
elif py_nm=='34':
    from .py34.slvs import *
from .pyslvs_generate.lib import *
