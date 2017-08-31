import numpy as np 
import networkx as nx

import matplotlib.pyplot as plt

from numpy.random import * 
# random() generates r in [0,1]

'''
S: Spreader -- red
I: Ignorant -- green
R: Stifler  -- grey
'''

lamda = 0.8 #S --> R 0.2
alpha = 0.8 #I --> know the idea 0.4
p = 0.8     #(spread it|know the idea) 0.2
G_BA = nx.barabasi_albert_graph(n=20,m=3,seed=2017)

seed(2017)


class InfoSpreadNet(nx.Graph):
	def __init__(self,G_edgelist):
		super(InfoSpreadNet, self).__init__(G_edgelist)

	def set_seed(self, seed_list=[1]):
		for i in self.nodes():
			self.node[i]['name'] = 'I'
			self.node[i]['next_name'] = 'I'
		
		for seed in seed_list:
			self.node[seed]['name'] = 'S'
			self.node[seed]['next_name'] = 'S'

	def FB_simulate(self):
		seeds = list(range(1,5))
		self.set_seed(seeds)

		count = {'S':len(seeds),'I':self.number_of_nodes()-len(seeds), 'R':0}
		print(count)
		print("=========================")

		t_max = 1000
		for time in range(t_max):
			for i in self.nodes():
			# while count['S'] > 0:
				if self.node[i]['name'] != 'S':
					continue
				# active: Speader
				for n in self.neighbors(i):
					# passive: Ignorant
					if self.node[n]['name'] != 'I':
						continue
					if random() < alpha:
					    # passive: I --> S or R
						if random() < p:
							# passive: I --> S
							self.node[n]['name'] = 'S'
							count['I'] -= 1
							count['S'] += 1 
							print(count)
						else:            
							# passive: I --> R
							self.node[n]['name'] = 'R'
							count['I'] -= 1
							count['R'] += 1
							print(count)

					# passive: Spreader or Stifler
					elif random() < lamda: 
						# active: S --> R
						self.node[i]['name'] = 'R'
						count['S'] -= 1
						count['R'] += 1
						print(count)
						if count['S'] == 0:
							spread_time = time
							return (self, spread_time, count)


if __name__ == '__main__':
	net = InfoSpreadNet(G_BA.edges())
	net.FB_simulate()
	print(net.number_of_nodes())
























