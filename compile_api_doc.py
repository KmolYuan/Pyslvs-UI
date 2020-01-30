# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import get_type_hints, List, Dict, Iterator, Iterable, Any
from types import ModuleType
from os import walk
from os.path import join
from importlib import import_module
from pkgutil import walk_packages
from textwrap import dedent
from inspect import isfunction, isclass, getfullargspec, FullArgSpec


class StandardModule(ModuleType):
    __all__: List[str]
    __path__: List[str]


def get_name(obj: Any) -> str:
    """Get a real name from an object."""
    if hasattr(obj, '__name__'):
        return obj.__name__ if obj.__module__ == 'builtins' else obj.__module__ + '.' + obj.__name__
    elif type(obj) is str:
        return obj
    else:
        return repr(obj)


def public(obj: Any) -> Iterator[str]:
    """Yield public names only."""
    for name in dir(obj):
        if name == '__init__' or not name.startswith('_'):
            yield name


def doc_dedent(text: str) -> str:
    """Remove first indent of the docstring."""
    two_parts = text.split('\n', maxsplit=1)
    if len(two_parts) == 2:
        return two_parts[0] + '\n' + dedent(two_parts[1])
    else:
        return text


def load_stubs(module: StandardModule) -> None:
    """Load all pyi files."""
    modules = []
    for root, _, files in walk(module.__path__[0]):
        for file in files:
            if not file.endswith('.pyi'):
                continue
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


def table_row(items: Iterable[str], space: bool = True) -> str:
    """Make a row of a Markdown table."""
    s = " " if space else ""
    return '|' + s + (s + '|' + s).join(items) + s + '|\n'


def table_line(items: Iterable[str]) -> str:
    """Make a line of a Markdown table."""
    return table_row((':' + '-' * (len(s) if len(s) > 3 else 3) + ':' for s in items), False)


def make_table(args: FullArgSpec) -> str:
    """Make an argument table for function or method."""
    args_doc = []
    type_doc = []
    all_args = []
    # Positional arguments
    all_args.extend(args.args or [])
    # The name of '*'
    if args.varargs is not None:
        new_name = f'**{args.varargs}'
        args.annotations[new_name] = args.annotations[args.varargs]
        all_args.append(new_name)
    elif args.kwonlyargs:
        all_args.append('*')
    # Keyword only arguments
    all_args.extend(args.kwonlyargs or [])
    # The name of '**'
    if args.varkw is not None:
        new_name = f'**{args.varkw}'
        args.annotations[new_name] = args.annotations[args.varkw]
        all_args.append(new_name)
    all_args.append('return')
    for arg in all_args:  # type: str
        args_doc.append(arg)
        if arg in args.annotations:
            type_doc.append(get_name(args.annotations[arg]))
        else:
            type_doc.append(" ")
    doc = table_row(args_doc) + table_line(args_doc) + table_row(type_doc)
    df = []
    if args.defaults is not None:
        df.extend([" "] * (len(args.args) - len(args.defaults)))
        df.extend(args.defaults)
    if args.kwonlydefaults is not None:
        df.extend(args.kwonlydefaults.get(arg, " ") for arg in args.kwonlyargs)
    if df:
        df.append(" ")
        doc += table_row(f"{v}" for v in df)
    doc += '\n'
    return doc


def switch_types(parent: Any, name: str, level: int, prefix: str = "") -> str:
    """Generate docstring by type."""
    obj = getattr(parent, name)
    doc = '#' * level + " "
    if prefix:
        doc += f"{prefix}."
    doc += f"{name}"
    sub_doc = []
    if isfunction(obj):
        doc += "()\n\n" + make_table(getfullargspec(obj))
    elif isclass(obj):
        doc += f"\n\nInherited from `{get_name(obj.__mro__[1])}`.\n\n"
        hints = get_type_hints(obj)
        if hints:
            title_doc, type_doc = zip(*hints.items())
            doc += (table_row(title_doc) + table_line(title_doc)
                    + table_row(get_name(v) for v in type_doc) + '\n')
        for attr_name in public(obj):
            if attr_name not in hints:
                sub_doc.append(switch_types(obj, attr_name, level + 1, name))
    elif hasattr(obj, '__call__'):
        doc += '()\n\n'
    else:
        doc += '\n\n'
        if hasattr(obj, '__name__'):
            hints = get_type_hints(parent)
            if obj.__name__ in hints:
                doc += (table_row(['type']) + table_line(['type'])
                        + table_row(get_name(hints[obj.__name__])))
    doc += doc_dedent(obj.__doc__ or "").rstrip()
    if sub_doc:
        doc += '\n\n' + '\n\n'.join(sub_doc)
    return doc


def find_objs(module: StandardModule) -> Iterator[str]:
    """Find all names and output doc."""
    load_stubs(module)
    for name in module.__all__:
        yield switch_types(module, name, 3).rstrip()


def replace_keywords(doc: str, ignore_module: List[str]) -> str:
    """Replace keywords from docstring."""
    for name in reversed(ignore_module):
        doc = doc.replace(name + '.', "")
    for word, re_word in (
        ('NoneType', 'None'),
        ('Ellipsis', '...'),
    ):
        doc = doc.replace(word, re_word)
    return doc


def root_module(name: str, module: str) -> str:
    """Root module docstring."""
    modules: List[StandardModule] = [import_module(module)]
    root_path = modules[0].__path__
    ignore_module = ['typing']
    for _, n, _ in walk_packages(root_path, module + '.'):  # type: str
        m = import_module(n)
        if hasattr(m, '__all__'):
            modules.append(m)
    ignore_module.extend(m.__name__ for m in modules)
    return f"# {name} API\n\n" + '\n\n'.join(
        f"## Module `{m.__name__}`\n\n{m.__doc__.rstrip()}\n\n"
        + replace_keywords('\n\n'.join(find_objs(m)), ignore_module)
        for m in modules
    )


def gen_api(root_names: Dict[str, str]) -> None:
    for name, module in root_names.items():
        print(root_module(name, module))


if __name__ == '__main__':
    gen_api({"Pyslvs": 'pyslvs', "Python-Solvespace": 'python_solvespace'})
