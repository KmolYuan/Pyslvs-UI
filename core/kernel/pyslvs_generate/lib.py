# -*- coding: utf-8 -*-
from ..pyVersion import py_nm
#SLVS Version & pyslvs_generate Version
if py_nm=='36w':
    from .py36w import tinycadlib
    from .py36w.planarlinkage import build_planar
    from .py36w.rga import Genetic
    from .py36w.firefly import Firefly
    from .py36w.de import DiffertialEvolution
elif py_nm=='35w':
    from .py35w import tinycadlib
    from .py35w.planarlinkage import build_planar
    from .py35w.rga import Genetic
    from .py35w.firefly import Firefly
    from .py35w.de import DiffertialEvolution
elif py_nm=='35':
    from .py35 import tinycadlib
    from .py35.planarlinkage import build_planar
    from .py35.rga import Genetic
    from .py35.firefly import Firefly
    from .py35.de import DiffertialEvolution
elif py_nm=='34':
    from .py34 import tinycadlib
    from .py34.planarlinkage import build_planar
    from .py34.rga import Genetic
    from .py34.firefly import Firefly
    from .py34.de import DiffertialEvolution
