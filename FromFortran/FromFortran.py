import networkx as nx
import numpy as np
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import info_spread
from data_preprocess import *
from tqdm import tqdm



G0, adjlist_m = reconstruct_adjlist('BA500.csv')
nodes_sorted_by_degree = degree_list(G0)
'''
Ignorant: 0
Spreader: 1
Stifler : 2
'''

def initialise(adjlist,seeds,nodes_to_rm):
    states = np.zeros(adjlist.shape[0],dtype=np.int32)
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
        states[int(i)] = -1
    return adjlist,states

def InfoSpread(adjlist,seeds,nodes_to_rm):
    change = 1 
    adjlist, states = initialise(adjlist,seeds,nodes_to_rm)

    while change:
        states,change = info_spread._info_spread(adjlist, states)
    return states

# np.random.seed(2017)

def main_simulate(adjlist, nodes_to_rm):
    N = adjlist.shape[0]
    rm_nodes = []
    Avr_rhos = []
    # for i in tqdm(nodes_to_rm):
    for i in nodes_to_rm:
        rm_nodes.append(i)
        rho = 0
        # for seed in range(N):
        #     final_states = InfoSpread(adjlist, [seed], rm_nodes)
        #     rho += sum(np.where(np.array(final_states) == 2, 1, 0))/N
        # rho=rho/500
        for seed in range(N):
            for s in range(100):
                final_states = InfoSpread(adjlist, [seed], rm_nodes)
                rho += sum(np.where(np.array(final_states) == 2, 1, 0))/N
        rho=rho/500/100
        
        Avr_rhos.append(rho)
        
    plt.plot(range(25), Avr_rhos,'ro')
    # plt.savefig("AR.png")
    plt.show()

if __name__ == '__main__':
    attack_list_degree = np.array(nodes_sorted_by_degree)[:25,0]
    main_simulate(adjlist_m,attack_list_degree)