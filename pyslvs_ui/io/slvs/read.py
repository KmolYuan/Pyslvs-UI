# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List, Set, Dict
from pyslvs import VLink


class SlvsParser:
    """Use to read data from solvespace file format."""
    groups: List[Dict[str, str]]
    requests: List[Dict[str, str]]
    entities: List[Dict[str, str]]
    constraints: List[Dict[str, str]]

    def __init__(self, file_name: str):
        """Open the file when initialize."""
        self.groups = []
        self.requests = []
        self.entities = []
        self.constraints = []
        dataset: Dict[str, List[Dict[str, str]]] = {
            'AddGroup': self.groups,
            'AddParam': [],
            'AddRequest': self.requests,
            'AddEntity': self.entities,
            'AddConstraint': self.constraints,
        }
        args: Dict[str, str] = {}
        with open(file_name, 'r', encoding="iso-8859-15") as f:
            if f.readline() != "±²³SolveSpaceREVa\n":
                return
            for line in f:
                if line == '\n':
                    args = {}
                elif '=' in line:
                    attribute, data = line[:-1].split('=')
                    args[attribute] = data
                elif line[:-1] in dataset:
                    dataset[line[:-1]].append(args)

    def is_valid(self) -> bool:
        """Simple check whether if file is valid."""
        return bool(self.groups)

    def get_groups(self) -> List[Tuple[str, str]]:
        """Read and return group names."""
        groups = []
        for group in self.groups:
            # Number code and group name
            groups.append((
                group['Group.h.v'],
                "".join(x for x in group['Group.name'] if x.isalnum() or x in "._- ")
            ))
        return groups[1:]

    def parse(self, group: str) -> str:
        """Parse as PMKS expression for specified group.

        + Requests: Get all links.
            + Independence points will be ignored.
        + Constraint: Adjacency.
            + Collecting links for each point.
        + Entities: Get positions.
        """

        def int16(n: str) -> int:
            """Generate 16 bit interger."""
            return int(n, 16)

        # Requests: Get all links
        requests = []
        for request in self.requests:
            if request['Request.group.v'] == group:
                # 0x4 << 16 == 0x40000
                requests.append(int16(request['Request.h.v']) << 16)

        links: Dict[int, Set[int]] = {link: {link + 1, link + 2} for link in requests}
        links[0] = set()

        # Constraint: Adjacency
        # Grounded. Other links at least will greater than 4
        for constraint in self.constraints:
            if constraint['Constraint.group.v'] != group:
                continue
            if constraint['Constraint.type'] == '20':
                now_replace = int16(constraint['Constraint.ptA.v'])
                for vlink in links.values():
                    num = int16(constraint['Constraint.ptB.v'])
                    if num in vlink:
                        vlink.remove(num)
                        vlink.add(now_replace)
            elif constraint['Constraint.type'] == '31':
                links[0].add(int16(constraint['Constraint.ptA.v']))

        pos: Dict[int, Tuple[str, str]] = {}
        for vlink in links.values():
            for point in vlink:
                if point not in pos:
                    pos[point] = ('0', '0')

        # Entities: Get positions
        for entity in self.entities:
            if entity['Entity.type'] != '2001':
                continue
            num = int16(entity['Entity.h.v'])
            if num in pos:
                pos[num] = (
                    entity.get('Entity.actPoint.x', '0'),
                    entity.get('Entity.actPoint.y', '0'),
                )

        # Rename link names
        vlinks = {}
        for i, name in enumerate(sorted(links)):
            if i == 0:
                vlinks[VLink.FRAME] = links.pop(name)
            else:
                vlinks[f'link_{i - 1}'] = links.pop(name)
        exprs = []
        for num in sorted(pos):
            x, y = pos[num]
            links_str = ", ".join(name for name, link in vlinks.items() if num in link)
            exprs.append(f"J[R, color[Green], P[{x}, {y}], L[{links_str}]]")
        return "M[" + ", ".join(exprs) + "]"
