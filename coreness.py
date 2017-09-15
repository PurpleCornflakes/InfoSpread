# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

# change defaults to be less ugly
mpl.rc('xtick', labelsize=14, color="#222222") 
mpl.rc('ytick', labelsize=14, color="#222222") 
mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
mpl.rc('font', size=16)
mpl.rc('xtick.major', size=6, width=1)
mpl.rc('xtick.minor', size=3, width=1)
mpl.rc('ytick.major', size=6, width=1)
mpl.rc('ytick.minor', size=3, width=1)
mpl.rc('axes', linewidth=1, edgecolor="#222222", labelcolor="#222222")
mpl.rc('text', usetex=False, color="#222222")


G = nx.read_adjlist('/Users/qinglingzhang/network_ER200.csv', comments='#',create_using=nx.Graph(), delimiter=',', nodetype=int, encoding='utf-8')

G.remove_node(0)
N=len(G)
L=G.size()


g_cores=list(nx.core_number(G).values())
g_ci=list(nx.clustering(G).values())
g_degrees=list(G.degree().values())

kcoremax=max(g_cores)
G_assort=nx.degree_assortativity_coefficient(G)
G_cluster=nx.average_clustering(G)

file=open('ER.txt','w')
txt = 'ER4000_Assortativity='+str(G_assort)+'\n' + 'ER4000_avrCluster='+str(G_cluster)+'\n'
file.write(txt)
file.close

# fig=plt.figure(figsize=(8,8))
# nx.draw_spring(G,node_size=40)#spring/circular


fig1 = plt.figure(figsize=(6,4))

# x should be midpoint of each bin
bins=np.arange(0.5,kcoremax+1.5,1) 
# histogram the data
plt.hist(g_cores,bins, histtype="stepfilled",normed=True, color="#C1F320" , alpha=.5)
plt.xlabel(r"$k-core$", fontsize=16)
plt.ylabel(r"$P(k)$", fontsize=16)

# remove right and top boundaries because they're ugly
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

#Save and Show the plot
plt.savefig("ER4000.png")
plt.show()
