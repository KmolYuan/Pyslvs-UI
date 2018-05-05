# -*- coding: utf-8 -*-
#cython: language_level=3

"""Triangular expressions."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from typing import Sequence, Iterator
from libc.math cimport sin, cos
import numpy as np
cimport numpy as np
from tinycadlib cimport VPoint
from cpython cimport bool


cdef inline bool isAllLock(dict status, dict same={}):
    """Test is all status done."""
    cdef int node
    cdef bool n_status
    for node, n_status in status.items():
        if (not n_status) and (node not in same):
            return False
    return True


cdef inline bool clockwise(tuple c1, tuple c2, tuple c3):
    """Check orientation of three points."""
    cdef double val = (c2[1] - c1[1])*(c3[0] - c2[0]) - (c2[0] - c1[0])*(c3[1] - c2[1])
    return ((val == 0) or (val > 0))


ctypedef fused sequence:
    list
    tuple


def _get_reliable_friend(
    node: int,
    vpoints: Sequence[VPoint],
    vlinks: dict,
    status: dict
) -> Iterator[int]:
    """Return a generator yield the nodes
        that has solution on the same link.
    """
    cdef str link
    cdef int friend
    for link in vpoints[node].links:
        if len(vlinks[link]) < 2:
            continue
        for friend in vlinks[link]:
            if status[friend] and (friend != node):
                yield friend


def _get_notbase_friend(
    node: int,
    vpoints: Sequence[VPoint],
    vlinks: dict,
    status: dict
) -> Iterator[int]:
    """Get a friend from constrained nodes."""
    if len(vpoints[node].links) < 2:
        raise StopIteration
    cdef int friend
    for friend in vlinks[vpoints[node].links[1]]:
        yield friend


def _get_base_friend(
    node: int,
    vpoints: Sequence[VPoint],
    vlinks: dict,
    status: dict
) -> Iterator[int]:
    """Get the constrained node of same linkage."""
    if len(vpoints[node].links) < 1:
        raise StopIteration
    cdef int friend
    for friend in vlinks[vpoints[node].links[0]]:
        yield friend


cdef inline int get_input_base(int node, sequence inputs):
    """Get the base node for input pairs."""
    cdef int base, node_
    for base, node_ in inputs:
        if node == node_:
            return base
    return -1


cpdef list vpoints_configure(sequence vpoints, sequence inputs, dict status = {}):
    """Auto configuration algorithm.
    
    For VPoint list.
    vpoints: [vpoint0, vpoint1, ...]
    inputs: [(p0, p1), (p0, p2), ...]
    
    Data:
    status: Dict[int, bool]
    """
    cdef VPoint vpoint
    cdef list pos = []
    for vpoint in vpoints:
        pos.append(vpoint.c[0] if (vpoint.type == 0) else vpoint.c[1])
    
    cdef dict vlinks = {}
    cdef int node
    cdef str link
    for node, vpoint in enumerate(vpoints):
        status[node] = False
        if vpoint.links:
            for link in vpoint.links:
                if ('ground' == link) and (vpoint.type == 0):
                    status[node] = True
                #Add as vlink.
                if link not in vlinks:
                    vlinks[link] = {node}
                else:
                    vlinks[link].add(node)
        else:
            status[node] = True
    
    cdef list exprs = []
    cdef int link_symbol = 0
    cdef int angle_symbol = 0
    
    cdef int base
    cdef set input_targets = {node for base, node in inputs}
    
    for base, node in inputs:
        if status[base]:
            exprs.append((
                'PLAP',
                'P{}'.format(base),
                'L{}'.format(link_symbol),
                'a{}'.format(angle_symbol),
                'P{}'.format(node),
            ))
            status[node] = True
            link_symbol += 1
            angle_symbol += 1
    
    node = 0
    cdef int friend_a, friend_b, friend_c, friend_d
    cdef bool not_grounded
    cdef int skip_times = 0
    cdef int around = len(status)
    cdef double tmp_x, tmp_y, angle
    cdef object f1
    while not isAllLock(status):
        
        if node not in status:
            node = 0
            continue
        
        #Check the solution.
        #If re-scan again.
        if skip_times >= around:
            break
        
        if status[node]:
            node += 1
            skip_times += 1
            continue
        
        if vpoints[node].type == 0:
            """R joint.
            
            + Is input node?
            + Normal revolute joint.
            """
            
            if node in input_targets:
                base = get_input_base(node, inputs)
                if status[base]:
                    exprs.append((
                        'PLAP',
                        'P{}'.format(base),
                        'L{}'.format(link_symbol),
                        'a{}'.format(angle_symbol),
                        'P{}'.format(node),
                    ))
                    status[node] = True
                    link_symbol += 1
                    angle_symbol += 1
                else:
                    skip_times += 1
            else:
                f1 = _get_reliable_friend(node, vpoints, vlinks, status)
                try:
                    friend_a = next(f1)
                    friend_b = next(f1)
                except StopIteration:
                    skip_times += 1
                else:
                    if not clockwise(
                        pos[friend_a],
                        pos[node],
                        pos[friend_b]
                    ):
                        friend_a, friend_b = friend_b, friend_a
                    exprs.append((
                        'PLLP',
                        'P{}'.format(friend_a),
                        'L{}'.format(link_symbol),
                        'L{}'.format(link_symbol + 1),
                        'P{}'.format(friend_b),
                        'P{}'.format(node),
                    ))
                    status[node] = True
                    link_symbol += 2
                    skip_times = 0
        
        elif vpoints[node].type == 1:
            """TODO: P joint."""
        
        elif vpoints[node].type == 2:
            """RP joint."""
            f1 = _get_base_friend(node, vpoints, vlinks, status)
            #Copy as 'friend_c'.
            friend_c = node
            #'S' point.
            tmp_x, tmp_y = pos[node]
            angle = np.deg2rad(vpoints[node].angle)
            tmp_x += cos(angle)
            tmp_y += sin(angle)
            try:
                friend_a = next(_get_notbase_friend(node, vpoints, vlinks, status))
                friend_b = next(f1)
                if 'ground' != vpoints[node].links[0]:
                    """Slot is not grounded."""
                    friend_d = next(f1)
                    if not clockwise(
                        pos[friend_b],
                        (tmp_x, tmp_y),
                        pos[friend_d]
                    ):
                        friend_b, friend_d = friend_d, friend_b
                    exprs.append((
                        'PLLP',
                        'P{}'.format(friend_b),
                        'L{}'.format(link_symbol),
                        'L{}'.format(link_symbol + 1),
                        'P{}'.format(friend_d),
                        'P{}'.format(node),
                    ))
                    link_symbol += 2
            except StopIteration:
                skip_times += 1
            else:
                """PLPP triangular.
                
                [PLLP]
                Set 'S' (slider) point to define second point of slider.
                + A 'friend' from base link.
                + Get distance from me and friend.
                
                [PLPP]
                Re-define coordinate of target point by self and 'S' point.
                + A 'friend' from other link.
                + Solving.
                """
                if not clockwise(
                    pos[friend_b],
                    (tmp_x, tmp_y),
                    pos[friend_c]
                ):
                    friend_b, friend_c = friend_c, friend_b
                exprs.append((
                    'PLLP',
                    'P{}'.format(friend_b),
                    'L{}'.format(link_symbol),
                    'L{}'.format(link_symbol + 1),
                    'P{}'.format(friend_c),
                    'S{}'.format(node),
                ))
                exprs.append((
                    'PLPP',
                    'P{}'.format(friend_a),
                    'L{}'.format(link_symbol + 2),
                    'P{}'.format(node),
                    'S{}'.format(node),
                    'P{}'.format(node),
                ))
                status[node] = True
                link_symbol += 3
                skip_times = 0
        
        node += 1
    """
    exprs: [('PLAP', 'P0', 'L0', 'a0', 'P1', 'P2'), ...]
    """
    return exprs
