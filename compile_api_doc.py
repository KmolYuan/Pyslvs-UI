# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, get_type_hints, List, Set, Dict, Iterable, Callable, Any
from types import ModuleType
from sys import stdout, modules as sys_modules
from os import listdir
from os.path import join, sep, splitext
from importlib import import_module
from pkgutil import walk_packages
from textwrap import dedent
from re import sub
from dataclasses import is_dataclass
from inspect import isfunction, isclass, isgenerator, getfullargspec
from logging import getLogger, basicConfig, DEBUG

__all__ = ['gen_api']

loaded_path: Set[str] = set()
unload_modules = set(sys_modules)
basicConfig(stream=stdout, level=DEBUG, format="%(message)s")
logger = getLogger()


class StandardModule(ModuleType):
    __all__: List[str]
    __path__: List[str]


def get_name(obj: Any) -> str:
    """Get a real name from an object."""
    if hasattr(obj, '__name__'):
        if hasattr(obj, '__module__') and not hasattr(obj, '__class__'):
            if obj.__module__ == 'builtins':
                return obj.__name__
            else:
                return f"{obj.__module__}.{obj.__name__}"
        return obj.__name__
    elif type(obj) is str:
        return obj
    else:
        return repr(obj)


def to_module(path: str) -> str:
    """Turn to Python module name."""
    path, _ = splitext(path)
    return path.replace(sep, '.')


def public(names: Iterable[str], init: bool = True) -> Iterable[str]:
    """Yield public names only."""
    for name in names:
        if init:
            init = name == '__init__'
        if init or not name.startswith('_'):
            yield name


def docstring(obj: object) -> str:
    """Remove first indent of the docstring."""
    doc = obj.__doc__
    if doc is None:
        return ""
    two_parts = doc.split('\n', maxsplit=1)
    if len(two_parts) == 2:
        doc = two_parts[0] + '\n' + dedent(two_parts[1])
    return doc.lstrip().rstrip()


def table_row(*items: Iterable[str]) -> str:
    """Make the rows to a pipe table."""

    def table(_items: Iterable[str], space: bool = True) -> str:
        s = " " if space else ""
        return '|' + s + (s + '|' + s).join(_items) + s + '|\n'

    if len(items) == 0:
        raise ValueError("the number of rows is not enough")
    doc = table(items[0])
    if len(items) == 1:
        return doc
    line = (':' + '-' * (len(s) if len(s) > 3 else 3) + ':' for s in items[0])
    doc += table(line, False)
    for item in items[1:]:
        doc += table(item)
    return doc


def make_table(obj: Callable) -> str:
    """Make an argument table for function or method."""
    args = getfullargspec(obj)
    hints = get_type_hints(obj)
    args_doc = []
    type_doc = []
    all_args = []
    # Positional arguments
    all_args.extend(args.args or [])
    # The name of '*'
    if args.varargs is not None:
        new_name = f'**{args.varargs}'
        hints[new_name] = hints[args.varargs]
        all_args.append(new_name)
    elif args.kwonlyargs:
        all_args.append('*')
    # Keyword only arguments
    all_args.extend(args.kwonlyargs or [])
    # The name of '**'
    if args.varkw is not None:
        new_name = f'**{args.varkw}'
        hints[new_name] = hints[args.varkw]
        all_args.append(new_name)
    all_args.append('return')
    for arg in all_args:  # type: str
        args_doc.append(arg)
        if arg in hints:
            type_doc.append(get_name(hints[arg]))
        else:
            type_doc.append(" ")
    doc = table_row(args_doc, type_doc)
    df = []
    if args.defaults is not None:
        df.extend([" "] * (len(args.args) - len(args.defaults)))
        df.extend(args.defaults)
    if args.kwonlydefaults is not None:
        df.extend(args.kwonlydefaults.get(arg, " ") for arg in args.kwonlyargs)
    if df:
        df.append(" ")
        doc += table_row([f"{v}" for v in df])
    return doc + '\n'


def is_staticmethod(parent: type, obj: Any) -> bool:
    """Return True if it is a static method."""
    return type(parent.__dict__[get_name(obj)]) is staticmethod


def switch_types(parent: Any, name: str, level: int, prefix: str = "") -> str:
    """Generate docstring by type."""
    obj = getattr(parent, name)
    doc = '#' * level + " "
    if prefix:
        doc += f"{prefix}."
    doc += f"{name}"
    sub_doc = []
    if isfunction(obj) or isgenerator(obj):
        doc += "()\n\n" + make_table(obj)
        if isclass(parent) and is_staticmethod(parent, obj):
            doc += "\nIs a static method.\n\n"
    elif isclass(obj):
        doc += f"\n\nInherited from `{get_name(obj.__mro__[1])}`."
        is_data_cls = is_dataclass(obj)
        if is_data_cls:
            doc += " Is a data class."
        doc += '\n\n'
        hints = get_type_hints(obj)
        if hints:
            title_doc, type_doc = zip(*hints.items())
            doc += table_row(title_doc, [get_name(v) for v in type_doc]) + '\n'
        for attr_name in public(dir(obj), not is_data_cls):
            if attr_name not in hints:
                sub_doc.append(switch_types(obj, attr_name, level + 1, name))
    elif callable(obj):
        doc += '()\n\n' + make_table(obj)
    elif type(obj) is property:
        doc += "\n\nIs a property.\n\n"
    else:
        return ""
    doc += docstring(obj)
    if sub_doc:
        doc += '\n\n' + '\n\n'.join(sub_doc)
    return doc


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


def import_from(name: str) -> StandardModule:
    """Import the module from name."""
    try:
        return cast(StandardModule, import_module(name))
    except ImportError:
        logger.warn(f"load module failed: {name}")
        return StandardModule(name)


def load_file(code: str, mod: ModuleType) -> bool:
    """Load file into the module."""
    try:
        sys_modules[get_name(mod)] = mod
        exec(compile(code, '', 'exec', flags=annotations.compiler_flag), mod.__dict__)
    except ImportError:
        return False
    except Exception as e:
        logger.debug(code)
        raise e
    return True


def load_stubs(m: StandardModule) -> None:
    """Load all pyi files."""
    modules = {}
    root = m.__path__[0]
    if root in loaded_path:
        return
    loaded_path.add(root)
    for file in listdir(root):
        if not file.endswith('.pyi'):
            continue
        with open(join(root, file), 'r', encoding='utf-8') as f:
            code = f.read()
        modules[get_name(m) + '.' + file[:-len('.pyi')]] = code
    module_names = list(modules)
    while module_names:
        name = module_names.pop()
        logger.debug(f"Load stub: {name}")
        code = modules[name]
        mod = ModuleType(name)
        if not load_file(code, mod):
            module_names.insert(0, name)
    # Reload root module
    name = get_name(m)
    with open(m.__file__, 'r', encoding='utf-8') as f:
        load_file(f.read(), m)
    sys_modules[name] = m


def get_level(name: str) -> int:
    """Return the level of the module name."""
    return name.count('.')


def load_root(root_name: str, root_module: str) -> str:
    """Root module docstring."""
    modules = {root_name: import_from(root_module)}
    root_path = modules[root_name].__path__
    ignore_module = ['typing', root_module]
    for info in walk_packages(root_path, root_module + '.'):
        m = import_from(info.name)
        del sys_modules[info.name]
        name = get_name(m)
        ignore_module.append(name)
        if hasattr(m, '__all__'):
            modules[name] = m
    doc = f"# {root_name} API\n\n"
    for n in sorted(modules, key=get_level, reverse=True):
        load_stubs(modules[n])
    for n in sorted(modules, key=get_level):
        m = modules[n]
        doc += f"## Module `{get_name(m)}`\n\n{docstring(m)}\n\n"
        doc += replace_keywords('\n\n'.join(
            switch_types(m, name, 3) for name in public(m.__all__)
        ), ignore_module) + '\n\n'
    return doc[:-2]


def gen_api(root_names: Dict[str, str], prefix: str) -> None:
    for name, module in root_names.items():
        path = join(prefix, f"{module.replace('_', '-')}-api.md")
        logger.debug(f"Write file: {path}")
        doc = load_root(name, module)
        logger.debug(sub(r"\n\n+", "\n\n", doc))
        # Unload modules
        for m_name in set(sys_modules) - unload_modules:
            del sys_modules[m_name]


def main() -> None:
    """Main function."""
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Compile Python public API into Generic Markdown.",
        epilog=f"{__copyright__} {__license__} {__author__} {__email__}"
    )
    parser.add_argument(
        'module',
        default=None,
        nargs='+',
        type=str,
        help="the module name that installed or in the current path, "
             "syntax real_name=module_name can specify a package name for it"
    )
    parser.add_argument(
        '-d',
        '--dir',
        metavar="DIR",
        default='docs',
        nargs='?',
        type=str,
        help="output to a specific directory"
    )
    arg = parser.parse_args()
    root_names = {}
    for m in arg.module:  # type: str
        n = m.split('=', maxsplit=1)
        if len(n) == 1:
            n.append(n[0])
        if n[1] == "":
            n[1] = n[0]
        root_names[n[0]] = n[1]
    gen_api(root_names, arg.dir)


if __name__ == '__main__':
    main()
