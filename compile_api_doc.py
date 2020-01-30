# -*- coding: utf-8 -*-

"""Compile documentation from modules."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import get_type_hints, List, Dict, Iterator, Iterable, Any
from types import ModuleType
from sys import stdout
from os import walk
from os.path import join
from importlib import import_module
from pkgutil import walk_packages
from textwrap import dedent
from inspect import isfunction, isclass, getfullargspec, FullArgSpec
from logging import getLogger, basicConfig, DEBUG

__all__ = ['gen_api']

basicConfig(stream=stdout, level=DEBUG, format="%(message)s")
logger = getLogger()


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


def public(names: Iterable[str]) -> Iterator[str]:
    """Yield public names only."""
    for name in names:
        if name == '__init__' or not name.startswith('_'):
            yield name


def docstring(text: str) -> str:
    """Remove first indent of the docstring."""
    two_parts = text.split('\n', maxsplit=1)
    if len(two_parts) == 2:
        text = two_parts[0] + '\n' + dedent(two_parts[1])
    return text.lstrip().rstrip()


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
            logger.error(code, exc_info=e)


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
    doc += docstring(obj.__doc__ or "")
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
    doc = f"# {name} API\n\n"
    for m in modules:
        load_stubs(m)
        doc += f"## Module `{m.__name__}`\n\n{docstring(m.__doc__)}\n\n"
        doc += replace_keywords('\n\n'.join(
            switch_types(m, name, 3) for name in public(m.__all__)
        ), ignore_module)
        doc += '\n\n'
    return doc[:-2]


def gen_api(root_names: Dict[str, str], prefix: str) -> None:
    for name, module in root_names.items():
        path = join(prefix, f"{module.replace('_', '-')}-api.md")
        logger.debug(f"Write file: {path}")
        logger.debug(root_module(name, module))


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
