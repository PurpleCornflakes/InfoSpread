import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import random

G = nx.read_adjlist('/Users/qinglingzhang/network_ER200.csv', comments='#',create_using=nx.Graph(), delimiter=',', nodetype=int, encoding='utf-8')
G.remove_node(0)
G0=G.copy() #graph not to be assortativity_preserving rewired
G0_assort=nx.degree_assortativity_coefficient(G0)
L=G0.number_of_edges()

#N=len(G)
#g_degrees=list(G.degree().values())
#kmax=max(g_degrees)

rew=L*100  #rew=L/2.0*math.log(1000000)
n=0

while n < rew:
    edgelist=nx.edges(G)
    p1=random.choice(edgelist)
    p2=random.choice(edgelist)
    a,b,c,d=p1[0],p1[1],p2[0],p2[1]

    if (a != c) & (b != d) & (a != d) & (b != c):#if nodes in pairs overlap, do nothing
        if (G.degree(a) == G.degree(d)) | (G.degree(b) == G.degree(c)):
            if (G.has_edge(a,c) == 0) & (G.has_edge(b,d) == 0):
                G.remove_edge(a,b)
                G.remove_edge(c,d)
                G.add_edge(a,c)
                G.add_edge(b,d)
                n+=1

        elif (G.degree(a) == G.degree(c)) | (G.degree(b) == G.degree(d)):
            if (G.has_edge(a,d) == 0) & (G.has_edge(b,c) == 0):
                G.remove_edge(a,b)
                G.remove_edge(c,d)
                G.add_edge(a,d)
                G.add_edge(b,c)
                n+=1

G_assort=nx.degree_assortativity_coefficient(G)
print G0.number_of_edges(),G.number_of_edges()

print G0_assort,G_assort