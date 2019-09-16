# -*- coding: utf-8 -*-

"""Launch script from module level."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

if __name__ == '__main__':
    from os.path import abspath, dirname
    import sys
    sys.path.append(abspath(dirname(__file__) + "/.."))
    from pyslvs_ui import main
    main()
