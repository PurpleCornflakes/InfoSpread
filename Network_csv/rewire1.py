from __future__ import print_function
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import csv


G = nx.read_adjlist('/Users/qinglingzhang/network_FB4000.csv', comments='#',create_using=nx.Graph(), delimiter=',', nodetype=int, encoding='utf-8')
G.remove_node(0)

G_assort=nx.degree_assortativity_coefficient(G)
N=len(G)
L=G.size()
g_degrees=list(G.degree().values())
kmax=max(g_degrees)




rew=L*100  
#rew=L/2.0*math.log(1000000)
G1=G.copy() #graph to be degree_preserving rewired
nx.connected_double_edge_swap(G1,nswap=rew,_window_threshold=3)

nx.write_adjlist(G1,"FB4000_rew1.csv")
#delete the first column so that RD.f90 could use the network directly.
def del_cvs_col(fname, newfname, idxs, delimiter=' '):
    with open(fname) as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=',')
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)
        
del_cvs_col('FB4000_rew1.csv', 'FB4000_rew1f.csv', [0])

#generate corelist

data=nx.core_number(G)
f1=open('coreness_FB4000_rew1.csv', 'w')
for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    print("%s,%s" % (key, value), file=f1)
f1.close()





