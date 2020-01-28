# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import get_type_hints, List, Iterator, Iterable, Any
from types import ModuleType
from os import walk
from os.path import join
from importlib import import_module
from pkgutil import walk_packages
from textwrap import dedent
from inspect import isfunction, isclass, getfullargspec, FullArgSpec


class StandardModule(ModuleType):
    __all__: List[str] = ...
    __path__: List[str] = ...


def get_name(obj: Any) -> str:
    """Get a real name from an object."""
    if hasattr(obj, '__name__'):
        return obj.__name__ if obj.__module__ == 'builtins' else obj.__module__ + '.' + obj.__name__
    else:
        return repr(obj)


def public(names: Iterable[str]) -> Iterator[str]:
    """Yield public names only."""
    yield from (name for name in names if not name.startswith('_'))


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
        for attr_name in public(dir(obj)):
            sub_doc.append(switch_types(obj, attr_name, level + 1, name))
    else:
        doc += '\n\n'
    doc += doc_dedent(obj.__doc__ or "")
    if sub_doc:
        doc += '\n\n' + '\n\n'.join(sub_doc)
    return doc


def find_objs(module: StandardModule) -> Iterator[str]:
    """Find all names and output doc."""
    if not hasattr(module, '__all__'):
        return
    load_stubs(module)
    for name in public(module.__all__):
        yield switch_types(module, name, 3).rstrip()


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
