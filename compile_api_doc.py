# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import get_type_hints, List, Iterator
from types import ModuleType
from importlib import import_module
from pkgutil import walk_packages
from inspect import isfunction, isclass


class StandardModule(ModuleType):
    __all__: List[str] = ...


def find_objs(module: StandardModule) -> Iterator[str]:
    """Find all names and output doc."""
    if not hasattr(module, '__all__'):
        return
    for name in module.__all__:
        if name.startswith('_'):
            continue
        obj = getattr(module, name)
        doc = ""
        if isfunction(obj):
            print(name, get_type_hints(obj))
        elif isclass(obj):
            for attr_name in dir(obj):
                if attr_name.startswith('_'):
                    continue
                #print(getattr(obj, attr_name))
        doc += obj.__doc__
        yield doc


def gen_api(root_name: str):
    root_module = import_module(root_name)
    doc = '\n\n'.join(find_objs(root_module))
    # For submodule
    root_path = root_module.__path__
    for _, name, _ in walk_packages(root_path, root_name + '.'):  # type: str
        m = import_module(name)
        doc += '\n\n'.join(find_objs(m))


if __name__ == '__main__':
    gen_api('pyslvs')
    gen_api('python_solvespace')
