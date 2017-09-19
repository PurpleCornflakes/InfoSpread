# import csv

# with open('ER200.csv',newline='') as csvfile:
# 	spamreader = csv.reader(csvfile, delimiter=' ')
# 	for row in spamreader:
# 		print(row)
# 		print('========')
import networkx as nx

G = nx.read_adjlist('/Users/qinglingzhang/AnomalousRobustness/Anomalous_robustness/network_BA200.csv', comments='#',create_using=nx.Graph(), delimiter=',', nodetype=int, encoding='utf-8')

G0 = nx.Graph()
print(type(G0))