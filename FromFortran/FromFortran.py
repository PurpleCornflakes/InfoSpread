import networkx as nx
import numpy as np
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import info_spread 


def construct():
    g = nx.read_edgelist('BA500_from0.csv',delimiter=",")
#     g = nx.barabasi_albert_graph(n=500, m=10,seed=2017)
    adjlist = nx.generate_adjlist(g, delimiter=",")
    adjlist = [np.array([eval(x)]).flatten() for x in adjlist]

    lens = [len(x) for x in adjlist]
    n = g.number_of_nodes()
    
    adjlist_m = np.ones([n, max(lens)], dtype = np.int32) * (-1)
    for nn in range(n):
        adjlist_m[nn, :lens[nn]] = adjlist[nn]
    
#     degree_list = [ [node,degree] for node, degree in g.degree(range(n)).items() ]
    degree_list = []
    for i in range(n):
        degree_list.append([i,sum(np.where(adjlist_m[i] != -1, 1, 0))-1])
#     print(degree_list)
    sorted_degrees = sorted(degree_list, key=itemgetter(1), reverse = True)
    return sorted_degrees,adjlist_m

sorted_degrees,adjlist_m = construct()

'''
Ignorant: 0
Spreader: 1
Stifler : 2
'''

def InfoSpread(adjlist, seeds, nodes_to_rm):
    N = adjlist.shape[0]
    change = 1 
    states = np.zeros(N,dtype=np.int32)
    
    # =================Initialize================
    '''
    rm nodes and set seeds --- Note: Don't set removed nodes as seeds
    '''
    # rm nodes from adjlist <=> set to -1
    for i in nodes_to_rm:
        for nns in adjlist[i,1:]:
            # disconnect i from its nns
            adjlist[nns,:] = np.where(adjlist[nns,:]==i, -1, adjlist[nns,:])
        # disconnect i and its nns
        adjlist[i,:] = -1

    #set seeds
    for seed in seeds:
        states[seed] = 1
    #rm nodes
    for i in nodes_to_rm:
        states[i] = -1
        
    
    #==============iter til converge==============
    while change:
        states,change = info_spread._info_spread(adjlist, states)
        
    return states


# np.random.seed(2017)

def main_simulate(adjlist, nodes_to_rm):
    N = adjlist.shape[0]
    rm_nodes = []
    Avr_rhos = []
    # kk = 0
    for i in nodes_to_rm:
        rm_nodes.append(i)
        rho = 0
        # for seed in range(N):
        #     final_states = InfoSpread(adjlist, [seed], rm_nodes)
        #     rho += sum(np.where(np.array(final_states) == 2, 1, 0))/N
        # rho=rho/500
        for seed in range(N):
            for s in range(100):
                # if kk % (N*100*len(nodes_to_rm)//1000) == 0:
                #     print("{} / {}".format(kk, N*100))
                # kk += 1
                final_states = InfoSpread(adjlist, [seed], rm_nodes)
                rho += sum(np.where(np.array(final_states) == 2, 1, 0))/N
        rho=rho/500/100
        
        Avr_rhos.append(rho)
        
    plt.plot(range(25), Avr_rhos,'ro')
    plt.savefig("AR.png")
    # plt.show()

if __name__ == '__main__':
    attack_list_k = np.array(sorted_degrees)[:25,0]
    main_simulate(adjlist_m,attack_list_k)