import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# G = nx.read_adjlist('/Users/qinglingzhang/network_ER200.csv', comments='#',create_using=nx.Graph(), delimiter=',', nodetype=int, encoding='utf-8')
# G.remove_node(0)

G = nx.barabasi_albert_graph(30,3)

N=len(G)
L=G.size()


g_cores=list(nx.core_number(G).values())
g_ci=list(nx.clustering(G).values())
g_degrees=list(G.degree().values())

kcoremax=max(g_cores)
G_assort=nx.degree_assortativity_coefficient(G)
G_cluster=nx.average_clustering(G)

# file=open('ER.txt','w')
# txt = 'ER4000_Assortativity='+str(G_assort)+'\n' + 'ER4000_avrCluster='+str(G_cluster)+'\n'
# file.write(txt)
# file.close


fig1 = plt.figure(figsize=(6,4))

# x should be midpoint of each bin
bins=np.arange(0.5,kcoremax+1.5,1) 
# histogram the data
plt.hist(g_cores,bins, histtype="stepfilled",normed=True, color="#C1F320" , alpha=.5)
plt.xlabel(r"$k-core$", fontsize=16)
plt.ylabel(r"$P(k)$", fontsize=16)


#Save and Show the plot
# plt.savefig("ER4000.png")
plt.show()
