# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Iterator, Any
from types import ModuleType
from os import walk
from os.path import join
from importlib import import_module
from pkgutil import walk_packages
from inspect import isfunction, isclass, getfullargspec, FullArgSpec


def iscythonfunction(obj: Any) -> bool:
    """Return true if the object is Cython function or method."""
    return type(obj).__name__ == 'cython_function_or_method'


class StandardModule(ModuleType):
    __all__: List[str] = ...
    __path__: List[str] = ...


def load_stubs(module: StandardModule) -> None:
    """Load all pyi files."""
    modules = []
    for root, _, files in walk(module.__path__[0]):
        for file in files:
            if file.endswith('.pyi'):
                with open(join(root, file), 'r', encoding='utf-8') as f:
                    code = f.read()
                code_list = code.splitlines()
                for line in reversed(range(len(code_list))):
                    if code_list[line].startswith("from ."):
                        code_list.pop(line)
                code = '\n'.join(code_list)
                modules.append(code)
    while modules:
        code = modules.pop()
        try:
            exec(code, module.__dict__)
        except NameError:
            modules.insert(0, code)
        except Exception as e:
            print(code)
            raise RuntimeError from e


def make_table(args: FullArgSpec) -> str:
    """Make an argument table for function or method."""
    args_doc = []
    type_doc = []
    default_doc = []
    if args.args is not None:
        for arg in args.args + ['return']:  # type: str
            args_doc.append(arg)
            type_obj = args.annotations[arg]
            if hasattr(type_obj, '__name__'):
                type_doc.append(type_obj.__name__)
            else:
                type_doc.append(repr(type_obj))
    doc = "| " + " | ".join(args_doc) + " |\n"
    doc += '|' + '|'.join(':' + '-' * len(a) + ':' for a in args_doc) + '|\n'
    doc += "| " + " | ".join(type_doc) + " |\n"
    if default_doc:
        doc += "| " + " | ".join(default_doc) + " |\n"
    doc += '\n'
    return doc


def find_objs(module: StandardModule) -> Iterator[str]:
    """Find all names and output doc."""
    if not hasattr(module, '__all__'):
        return
    load_stubs(module)
    for name in module.__all__:
        if name.startswith('_'):
            continue
        obj = getattr(module, name)
        doc = f"### {name}()\n\n"
        if isfunction(obj):
            doc += make_table(getfullargspec(obj))
        elif iscythonfunction(obj):
            doc += make_table(getfullargspec(obj))
        elif isclass(obj):
            for attr_name in dir(obj):
                if attr_name.startswith('_'):
                    continue
                doc += make_table(getfullargspec(getattr(obj, attr_name)))
        doc += obj.__doc__
        while doc.endswith('\n'):
            doc = doc[-1]
        yield doc


def gen_api(root_name: str) -> None:
    doc = ""
    modules: List[StandardModule] = [import_module(root_name)]
    root_path = modules[0].__path__
    for _, name, _ in walk_packages(root_path, root_name + '.'):  # type: str
        modules.append(import_module(name))
    for m in modules:
        doc += '\n\n'.join(find_objs(m))
    print(doc)


if __name__ == '__main__':
    gen_api('pyslvs')
    gen_api('python_solvespace')
