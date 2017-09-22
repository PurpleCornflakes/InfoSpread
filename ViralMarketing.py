'''
Simulate to find most influential spreaders
'''

import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import random # random_choice()
from tqdm import tqdm 
import sys # print to screen
import operator # sorting
from enum import * # for states S, I, R

class State(Enum):
	Susceptible = 0
	Infected = 1
	Removed = 2

def reset(G):
	nx.set_node_attributes(G, 'state', State.Susceptible)

def set_seeds_random(G, _num_seeds):
	nodes_to_infect = random.sample(G.nodes(), s_num_seeds)
	for n in nodes_to_infect:
		G.node[n]['state'] = State.Infected
	return nodes_to_infect

def set_seeds_degree(G, _num_seeds, largest = True):
	degrees = G.degree()
	nodes_to_infect = []
	nodes_sorted_by_degree = sorted(degrees.items(),key = operator.itemgetter(1), reverse = largest)
	for x in range(_num_seeds):
		nodes_to_infect.append(nodes_sorted_by_degree[x])
	for n in nodes_to_infect:
		G.node[n[0]]['state'] = State.Infected
	return nodes_to_infect

def transmission_model(beta = 0.03, alpha = 0.5):
	'''
	beta: infection rate
	alpha: removal rate
	return a infection model function
	'''
	def m(n,G):
		if G.node[n]['state'] == State.Susceptible:
			for k in G.neighbors(n):
				if G.node[k]['state'] == State.Susceptible and \
				random.random() <= beta:
					G.node[k]['state'] = State.Infected
				if random.random() <= alpha:
					G.node[n]['state'] = State.Removed
	return m

def execute_one_step(G, model):
	for n in G:
		model(n,G)

def get_states(G):
	infected = []
	susceptible = []
	removed = []
	for n in G:
		if G.node[n]['state'] == State.Infected:
			infected.append(n)
		elif G.node[n]['state'] == State.Susceptible:
			susceptible.append(n)
		else:
			removed.append(n)
	return susceptible, infected, removed

def print_states(G):
	s,i,r = get_states(G)
	print("S = %s, I = %s, R = %s"%(len(s),len(i),len(r)))

def run_spread_simulation(G, model, seeds, draw_G = False):
	'''
	return time series of S,I,R's respective num
	'''
	s_counts = []
	i_counts = []
	r_counts = []

	dt = 0
	s,i,r = get_states(G)

	pos = nx.spring_layout(G, k=0.75)

	while len(i) > 0:
		execute_one_step(G, model)
		s,i,r = get_states(G)
		s_counts.append(len(s))
		i_counts.append(len(i))
		r_counts.append(len(r))
		dt += 1
		sys.stderr.write('\r Infected: %d time step: %d'%(len(i),dt))
		sys.stderr.flush()
		if draw_G:
			draw_network_save(G, pos, dt, seeds)
	return s_counts, i_counts, r_counts, dt, seeds

def plot_infection(S,I,R,G):
	peak_incidence = max(I)
	peak_time = I.index(max(I))
	total_infected = S[0] - S[-1]

	fig_size = [18,13]
	plt.rcParams.update({'font.size':14,'figure.figsize':fig_size})
	xvalues = range(len(S))

	plt.plot(xvalues, S, 'g-', label = 'S')
	plt.plot(xvalues, I, 'b-', label = 'S')
	plt.plot(xvalues, R, 'r-', label = 'S')

	plt.axhline(peak_incidence, 'b--', label = 'Peak Incidence')
	plt.annotate(str(peak_incidence), xy = (1, peak_incidence+10),color = 'b')

	plt.axvline(peak_time, 'b:',label = 'Peak Time')
	plt.annotate(str(peak_time), xy = (peak_time+1, 8),color = 'b')

	plt.axhline(total_infected,'r--',label = 'Total Infected')
	plt.annotate(str(total_infected),xy = (1,total_infected+10),color = 'r')

	plt.legend()
	plt.xlabel = ('time step')
	plt.ylabel = ('Count')
	plt.title = ('SIR for network size'+str(G.order()))
	
	plt.show()

def draw_network_save(G, pos, t, seeds):
	states = []
	for n in G.nodes():
		if n in seeds:
			states.append(3)
		else:
			states.append(G.node[n]['state'])
	from matplotlib import colors
	cmap = colors.ListedColormap(['green','blue','red','yellow'])
	bounds = [0,1,2,3]

	nx.draw_networkx_nodes(G, pos, cmap = cmap, alpha = 0.5, node_size = 170, node_color = states)
	nx.draw_networkx_edges(G, pos, alpha = 0.5)
	plt.savefig("images/g"+str(t)+'.png')
	plt.clf()

def plotDistribution(_influences):
	plt.hist(_influences,range=[0,1],bins = 30)
	plt.title("Realisations")
	plt.xlabel("number of infected nodes / Total number of nodes")
	plt.ylabel('p')
	plt.show()

if __name__ = '__main__':
	N = 1000
	Gra = nx.barabasi_albert_graph(N, 3)

	m = transmission_model(0.08, 0.5)
	num_seeds = 5
	sampleSize = 20

	Influences = []
	for i in range(sampleSize):
		reset(Gra)
		seeds = set_seeds_random(Gra, num_seeds)
		S,I,R, endtime, ii = run_spread_simulation(Gra, m, seeds)
		Influences.append(float(R[-1])/len(Gra))

	print('the expected influence of the seed node is', np.average(Influences))
	plotDistribution(Influences)



# Influences = []
# for i in range(sampleSize):
# 	reset(Gra)
# 	seeds = set_seeds_degree(Gra, num_seeds)
# 	S, I, R, endtime, ii = run_spread_simulation(Gra, m, seeds)
# 	Influence.append(float(R[-1]/len(Gra)))

# 	print('the expected influence of the seed node is ',np.average(Influences))

# 	plotDistribution(Influences)



