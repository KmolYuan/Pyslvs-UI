# -*- coding: utf-8 -*-
from topologic import topo

print("Topologic test")
answer = topo([4, 2], degenerate=True)
#Show tree
for G in answer:
    print(G.edges)
    print('-'*7)
print("Answer count: {}".format(len(answer)))
