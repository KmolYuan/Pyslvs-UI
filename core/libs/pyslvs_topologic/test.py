# -*- coding: utf-8 -*-

if __name__=="__main__":
    print("Isomorphic test")
    from topologic import topo, Graph, GraphMatcher
    G = Graph([(0, 1), (0, 4), (1, 5), (2, 3), (2, 4), (3, 5), (4, 5)])
    H = Graph([(0, 2), (0, 4), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)])
    I = Graph([(0, 1), (0, 2), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)])
    GM_GH = GraphMatcher(G, H)
    print(GM_GH.is_isomorphic())
    GM_GI = GraphMatcher(G, I)
    print(GM_GI.is_isomorphic())
    print("Topologic test")
    answer, time = topo([4, 2], degenerate=True)
    #Show tree
    for G in answer:
        print(G.edges)
        print('-'*7)
    print("Answer count: {}, find in: {:.4f}[s]".format(len(answer), time))
    
    print('#'*7)
    
    print("Triangulation test")
    from triangulation import auto_configure
    from networkx import Graph
    #Test for 8-bar linkage.
    G = Graph([(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 4), (3, 5),
        (3, 7), (4, 6), (6, 7)])
    cus = {'P10': 7}
    same = {2: 1, 4: 3, 6: 7}
    status = {
        0: True,
        1: True,
        2: True,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False,
        8: False,
        9: False,
        10: False
    }
    pos = {
        0: (36.5, -59.5),
        1: (10.0, -94.12),
        2: (-28.5, -93.5),
        3: (102.5, -43.5),
        4: (77.5, -74.5),
        5: (28.82, -22.35),
        6: (23.5, 22.5),
        7: (-18.5, -44.5),
        8: (-75.5, -59.5),
        9: (56.5, 29.5),
        10: (68.5, 71.5),
        11: (-47.06, -28.24),
        12: (107.5, 42.5),
        13: (-109.41, -49.41),
        14: (44.12, 107.65)
    }
    Driver_list = ['P0']
    expr = auto_configure(G, cus, same, status, pos, Driver_list)
    print(expr)
    """
    [('PLAP', 'P0', 'L0', 'a0', 'P1', 'P3'),
    ('PLLP', 'P3', 'L1', 'L2', 'P1', 'P5'),
    ('PLLP', 'P3', 'L3', 'L4', 'P1', 'P7'),
    ('PLLP', 'P5', 'L5', 'L6', 'P1', 'P8'),
    ('PLLP', 'P7', 'L7', 'L8', 'P8', 'P9'),
    ('PLLP', 'P9', 'L9', 'L10', 'P7', 'P10')]
    """
