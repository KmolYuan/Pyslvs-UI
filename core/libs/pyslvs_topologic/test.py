# -*- coding: utf-8 -*-
from topologic import topo

if __name__=="__main__":
    print("Isomorphic test")
    from topologic import Graph, GraphMatcher
    G = Graph([(0, 1), (0, 4), (1, 5), (2, 3), (2, 4), (3, 5), (4, 5)])
    H = Graph([(0, 2), (0, 4), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)])
    I = Graph([(0, 1), (0, 2), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)])
    GM_GH = GraphMatcher(G, H)
    print(GM_GH.is_isomorphic())
    GM_GI = GraphMatcher(G, I)
    print(GM_GI.is_isomorphic())
    print("Topologic test")
    answer = topo([4, 2], degenerate=True)
    #Show tree
    for G in answer:
        print(G.edges)
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
