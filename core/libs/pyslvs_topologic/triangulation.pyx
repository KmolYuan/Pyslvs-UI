# -*- coding: utf-8 -*-

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from cpython cimport bool

cdef dict edges_view(object G):
    """This list can keep the numbering be consistent."""
    cdef int n
    cdef object e
    return {n: tuple(e) for n, e in enumerate(sorted(sorted(e) for e in G.edges))}

cdef bool isAllLock(dict status, dict same):
    """Test is all status done."""
    cdef int node
    cdef bool n_status
    for node, n_status in status.items():
        if (not n_status) and (node not in same):
            return False
    return True

def friends(
    object G,
    dict status,
    dict cus,
    dict same,
    int node1,
    bool reliable=False
):
    """Return a generator yield the nodes
    that has solution on the same link.
    """
    #All edges of all nodes.
    cdef dict edges = edges_view(G)
    cdef str n
    cdef int l
    for n, l in cus.items():
        edges[int(n.replace('P', ''))] = (l,)
    #Reverse dict of 'same'.
    cdef int v, k
    cdef dict same_r = {}
    for k, v in same.items():
        if v in same_r:
            same_r[v].append(k)
        else:
            same_r[v] = [k]
    #For all link of node1.
    cdef set links1 = set(edges[node1])
    #Second links of node1.
    cdef set links2
    cdef int node2, node3
    if node1 in same_r:
        for node2 in same_r[node1]:
            links1.update(edges[node2])
    #for all link.
    for node2 in edges:
        if (
            (node1 == node2) or
            (node2 in same) or
            (status[node2] != reliable)
        ):
            continue
        links2 = set(edges[node2])
        if node2 in same_r:
            for node3 in same_r[node2]:
                links2.update(edges[node3])
        #Reference by intersection and status.
        if links1 & links2:
            yield node2

cdef list sort_pos(object nodes, dict pos):
    """Sort points by position."""
    return sorted(nodes, key=lambda n: pos[n][0], reverse=True)

cpdef list auto_configure(
    object G,
    dict status,
    dict pos,
    object Driver_list,
    dict cus={},
    dict same={}
):
    """Auto configuration algorithm."""
    #Expression
    cdef list expr = []
    cdef int link_symbol = 0
    cdef int angle_symbol = 0
    #PLAP solutions.
    cdef int node, target_node
    cdef str point1, point2
    for point1 in Driver_list:
        node = int(point1.replace('P', ''))
        target_node = next(friends(G, status, cus, same, node))
        point2 = 'P{}'.format(target_node)
        expr.append((
            "PLAP",
            point1,
            'L{}'.format(link_symbol),
            'a{}'.format(angle_symbol),
            'P{}'.format(sort_pos(friends(G, status, cus, same, node, reliable=True), pos)[0]),
            point2
        ))
        link_symbol += 1
        angle_symbol += 1
        status[target_node] = True
    #PLLP solutions.
    node = 0
    cdef int skip_times = 0
    cdef int all_points_count = len(pos)
    cdef bool n_status
    cdef object rf
    cdef list two_friend
    while not isAllLock(status, same):
        if node not in pos:
            node = 0
            continue
        #Check the solution.
        if status[node] or (node in same):
            node += 1
            skip_times += 1
            #If re-scan again.
            if skip_times >= all_points_count:
                break
            continue
        rf = friends(G, status, cus, same, node, reliable=True)
        try:
            two_friend = sort_pos((next(rf), next(rf)), pos)
        except StopIteration:
            pass
        else:
            #Add solution.
            point = 'P{}'.format(node)
            expr.append((
                "PLLP",
                'P{}'.format(two_friend[0]),
                'L{}'.format(link_symbol),
                'L{}'.format(link_symbol + 1),
                'P{}'.format(two_friend[1]),
                point
            ))
            link_symbol += 2
            status[node] = True
        node += 1
        skip_times = 0
    return expr
