#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USAGE EXAMPLE:
# python graph_analyzer.py -n conversationName.graphml -v
# or to print results on file
# python graph_analyzer.py -n conversationName.graphml -v -f

import argparse
import networkx as nx
import numpy
from functions import *
# import matplotlib.pyplot as plt
# from termcolor import *

parser = argparse.ArgumentParser(description='Debug')
parser.add_argument("-n", required=True, help="Insert graphml file name to analize")
parser.add_argument("-v", action="store_true", help="Verbose mode for logging")
parser.add_argument("-f", action="store_true", help="Print results on file")
parser.add_argument("-m", default="w", help="File write mode ('a' to append or 'w' to overwrite)")
args = parser.parse_args()

G = nx.read_graphml("Graphs/"+args.n)
# nx.draw(G)
# plt.show()

users = []
tweets = []
attacks_in = []
attacks_out = []
defenses_in = []
defenses_out = []

for n1,n2,e in G.edges_iter(data=True):
	if e['edgeType']=='authorship':
		if n1 not in users:
			users.append(n1)
			tweets.append(1)
			attacks_in.append(0)
			attacks_out.append(0)
			defenses_in.append(0)
			defenses_out.append(0)
		else:
			tweets[users.index(n1)]+=1
	elif e['edgeType']=='attack':
		if G.node[n1]['author'] not in users:
			users.append(G.node[n1]['author'])
			tweets.append(0)
			attacks_in.append(0)
			attacks_out.append(1)
			defenses_in.append(0)
			defenses_out.append(0)
		else:
			attacks_out[users.index(G.node[n1]['author'])]+=1
		try:
			n2 = G.node[n2]['author']
		except:
			pass
		if n2 not in users:
			users.append(n2)
			tweets.append(0)
			attacks_in.append(1)
			attacks_out.append(0)
			defenses_in.append(0)
			defenses_out.append(0)
		else:
			attacks_in[users.index(n2)]+=1
	elif e['edgeType']=='defense':
		if G.node[n1]['author'] not in users:
			users.append(G.node[n1]['author'])
			tweets.append(0)
			attacks_in.append(0)
			attacks_out.append(0)
			defenses_in.append(0)
			defenses_out.append(1)
		else:
			defenses_out[users.index(G.node[n1]['author'])]+=1
		try:
			n2 = G.node[n2]['author']
		except:
			pass
		if n2 not in users:
			users.append(n2)
			tweets.append(0)
			attacks_in.append(0)
			attacks_out.append(0)
			defenses_in.append(1)
			defenses_out.append(0)
		else:
			defenses_in[users.index(n2)]+=1

# 11 Metrics
metrics = numpy.zeros(shape=(11,len(users)))

# first 8 metrics based on basic graph parameters
for i in range(0,len(users)):
	metrics[0][i]=tweets[i]/float(sum(tweets)) if tweets[i]>0 else 0

	metrics[1][i]=attacks_out[i]/float(tweets[i]) if tweets[i]>0 else 0
	metrics[2][i]=attacks_in[i]/float(tweets[i]) if tweets[i]>0 else 0

	metrics[3][i]=defenses_out[i]/float(tweets[i]) if tweets[i]>0 else 0
	metrics[4][i]=defenses_in[i]/float(tweets[i]) if tweets[i]>0 else 0

	metrics[5][i]=attacks_out[i]/float(defenses_out[i]) if defenses_out[i]>0 else 0
	metrics[6][i]=attacks_in[i]/float(defenses_in[i]) if defenses_in[i]>0 else 0

	metrics[7][i]=attacks_in[i]+attacks_out[i]+defenses_in[i]+defenses_out[i]

# % engagement and global score
for i in range(0,len(users)):
	metrics[8][i]=metrics[7][i]/float(sum(metrics[7]))
	metrics[9][i]=metrics[8][i]*metrics[0][i]

# normalized global score
for i in range(0,len(users)):
	metrics[10][i]=metrics[9][i]/max(metrics[9])


# network centralities

# centralities Matrix:		1) degree
#							2) in_degree
#							3) out_degree
#							4) eigenvector
#							5) closeness
#							6) betweenness
num_centralities = 6
centralitiesBasedOnUsers = numpy.zeros(shape=(num_centralities,len(users)))
centralitiesBasedOnTexts = numpy.zeros(shape=(num_centralities,len(users)))
error = False

for i in range(0,num_centralities):
	try:
		if i==0:
			c = nx.degree_centrality(G)
		elif i==1:
			c = nx.in_degree_centrality(G)
		elif i==2:
			c = nx.out_degree_centrality(G)
		elif i==3:
			c = nx.eigenvector_centrality_numpy(G)
		elif i==4:
			c = nx.closeness_centrality(G)
		elif i==5:
			c = nx.betweenness_centrality(G)
	except:
		error=True
		pass
	for nodeId, c_value in c.iteritems():
		if "t_" not in nodeId:	# User node
			centralitiesBasedOnUsers[i][users.index(nodeId)] = None if error else c_value
		else:					# Text node
			for n, d in G.nodes_iter(data=True):
				if nodeId==n:
					index = users.index(d['author'])
					centralitiesBasedOnTexts[i][index] += 0 if error else c_value
	error=False

# User text Reddit Score, User comment Karma and User link Karma
usersScore = numpy.zeros(len(users)) # Reddit users score as sum of all texts score
commentKarmas = numpy.zeros(len(users))
linkKarmas = numpy.zeros(len(users))

for n, d in G.nodes_iter(data=True):
	index = users.index(d['author'])
	if d['nodeType']=='text':
		index = users.index(d['author'])
		usersScore[index]+=int(d['score'])
	elif d['nodeType']=='user':
		try:
			commentKarmas[index]=int(d['commentKarma'])
		except:
			commentKarmas[index]=0
		try:
			linkKarmas[index]=int(d['linkKarma'])
		except:
			linkKarmas[index]=0

# Final results on file or console
if args.f:
	fileName = "Results/"+((args.n).split('_')[0])+".txt" if args.m=='a' else "Results/"+((args.n).split('.')[0])+".txt"
	f = open(fileName, args.m)
	f.write(((args.n).split('.')[0])+"\t\t\t\t\t\t"+
			"u.tw / c.tw\tu.atk_out / u.tw\tu.atk_in / u.tw\tu.def_out / u.tw\tu.def_in / u.tw\tu.atk_out / u.def_out\tu.atk_in / u.def_in\t"+
			"sum all atk and def\tEng. / tot. eng.\tEng. * Act.\tnorm(Eng. * Act.)\tDegree\tin Degree\tout Degree\tEigenvector\tCloseness\tBetweenness\tDegree-T\tin Degree-T\tout Degree-T\tEigenvector-T\tCloseness-T\tBetweenness-T\tSum of all Reddit Scores\tComment Karma\tLink Karma"+"\n"+
			"User\tTweets\tAtk_IN\tAtk_OUT\tDef_IN\tDef_OUT\tM0\tM1\tM2\tM3\tM4\tM5\tM6\tEngagement\t% Engagement\tGlobal Score\tNorm. GS\tD\tinD\toutD\tE\tC\tB\tD-T\tinD-T\toutD-T\tE-T\tC-T\tB-T\tRS\tC-Karma\tL-Karma\n")
	for i in range(0,len(users)):
		f.write(users[i]+"\t"+
				str(tweets[i])+"\t"+
				str(attacks_in[i])+"\t"+
				str(attacks_out[i])+"\t"+
				str(defenses_in[i])+"\t"+
				str(defenses_out[i])+"\t"+
				str(metrics[0][i])+"\t"+
				str(metrics[1][i])+"\t"+
				str(metrics[2][i])+"\t"+
				str(metrics[3][i])+"\t"+
				str(metrics[4][i])+"\t"+
				str(metrics[5][i])+"\t"+
				str(metrics[6][i])+"\t"+
				str(metrics[7][i])+"\t"+
				str(metrics[8][i])+"\t"+
				str(metrics[9][i])+"\t"+
				str(metrics[10][i])+"\t"+
				str(centralitiesBasedOnUsers[0][i])+"\t"+
				str(centralitiesBasedOnUsers[1][i])+"\t"+
				str(centralitiesBasedOnUsers[2][i])+"\t"+
				str(centralitiesBasedOnUsers[3][i])+"\t"+
				str(centralitiesBasedOnUsers[4][i])+"\t"+
				str(centralitiesBasedOnUsers[5][i])+"\t"+
				str(centralitiesBasedOnTexts[0][i])+"\t"+
				str(centralitiesBasedOnTexts[1][i])+"\t"+
				str(centralitiesBasedOnTexts[2][i])+"\t"+
				str(centralitiesBasedOnTexts[3][i])+"\t"+
				str(centralitiesBasedOnTexts[4][i])+"\t"+
				str(centralitiesBasedOnTexts[5][i])+"\t"+
				str(usersScore[i])+"\t"+
				str(commentKarmas[i])+"\t"+
				str(linkKarmas[i])+"\n")
	if args.m=='a':
		f.write("--- --- --- --- ---\n")
else:
	print "User\tTweets\tAtk_IN\tAtk_OUT\tDef_IN\tDef_OUT\tM0\tM1\tM2\tM3\tM4\tM5\tM6\tEngagement\t% Engagement\tGlobal Score\tNorm. GS\tD\tinD\toutD\tE\tC\tB\tD-T\tinD-T\toutD-T\tE-T\tC-T\tB-T\tRS\tC-Karma\tL-Karma"
	for i in range(0,len(users)):
		print 	(users[i]+"\t"+
				str(tweets[i])+"\t"+
				str(attacks_in[i])+"\t"+
				str(attacks_out[i])+"\t"+
				str(defenses_in[i])+"\t"+
				str(defenses_out[i])+"\t"+
				str(metrics[0][i])+"\t"+
				str(metrics[1][i])+"\t"+
				str(metrics[2][i])+"\t"+
				str(metrics[3][i])+"\t"+
				str(metrics[4][i])+"\t"+
				str(metrics[5][i])+"\t"+
				str(metrics[6][i])+"\t"+
				str(metrics[7][i])+"\t"+
				str(metrics[8][i])+"\t"+
				str(metrics[9][i])+"\t"+
				str(metrics[10][i])+"\t"+
				str(centralitiesBasedOnUsers[0][i])+"\t"+
				str(centralitiesBasedOnUsers[1][i])+"\t"+
				str(centralitiesBasedOnUsers[2][i])+"\t"+
				str(centralitiesBasedOnUsers[3][i])+"\t"+
				str(centralitiesBasedOnUsers[4][i])+"\t"+
				str(centralitiesBasedOnUsers[5][i])+"\t"+
				str(centralitiesBasedOnTexts[0][i])+"\t"+
				str(centralitiesBasedOnTexts[1][i])+"\t"+
				str(centralitiesBasedOnTexts[2][i])+"\t"+
				str(centralitiesBasedOnTexts[3][i])+"\t"+
				str(centralitiesBasedOnTexts[4][i])+"\t"+
				str(centralitiesBasedOnTexts[5][i])+"\t"+
				str(usersScore[i])+"\t"+
				str(commentKarmas[i])+"\t"+
				str(linkKarmas[i]))



