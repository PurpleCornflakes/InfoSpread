import csv
from operator import itemgetter
import numpy as np 
import networkx as nx
'''
add row # to the beginning of each row
'''
def add_column_to_csv(old_file_name='network_BA500.csv', new_file_name='BA500.csv'):
	old_file = open(old_file_name,'r') 
	new_file = open(new_file_name,'w')
	reader = csv.reader(old_file, delimiter = ',')
	writer = csv.writer(new_file, delimiter = ',')

	for i,row in enumerate(reader):
		row = [str(i+1)]+row
		writer.writerow(row)

	old_file.close()
	new_file.close()


def csv_minus_one(old_filename='BA500.csv', new_filename='BA500_new_adjlist.csv'):
	old_file = open(old_filename,'r') 
	new_file = open(new_filename,'w')
	reader = csv.reader(old_file, delimiter = ',')
	writer = csv.writer(new_file, delimiter = ',')

	for i,row in enumerate(reader):
		row = [str(int(x)-1) for x in row]
		writer.writerow([x for x in row if int(x) != -1])

	old_file.close()
	new_file.close()

'''
input old adjlist filename
construct new_adjlist padding with -1
'''
def reconstruct_adjlist(adjlist_file = 'network_BA500.csv',generate_BA = False):
	if generate_BA:
		g = nx.barabasi_albert_graph(n=500, m=10,seed=2017)

	else:
		add_column_to_csv()
		csv_minus_one()
		g = nx.read_adjlist('BA500_new_adjlist.csv',delimiter=",")

	adjlist = nx.generate_adjlist(g, delimiter=",")
	adjlist = [np.array([eval(x)]).flatten() for x in adjlist]

	lens = [len(x) for x in adjlist]
	n = g.order()

	new_adjlist = np.ones([n, max(lens)], dtype = np.int32) * (-1)
	for nn in range(n):
	    new_adjlist[nn, :lens[nn]] = adjlist[nn]
	return g,new_adjlist

# reconstruct_adjlist()

def degree_list(network):
	n = network.order()
	degrees = network.degree()
	degree_list = [ [node,degree] for node, degree in degrees.items() ]
	nodes_sorted_by_degree = sorted(degree_list, key=itemgetter(1), reverse = True)
	# print(nodes_sorted_by_degree)
	return np.array(nodes_sorted_by_degree)
