#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USAGE EXAMPLE:
# python graph_builder.py -n conversationName.csv -v

import argparse
import csv
from functions import *
from RedditText import RedditText

parser = argparse.ArgumentParser(description='Debug')
parser.add_argument("-n", required=True, help="Insert CSV file name to analize")
parser.add_argument("-v", action="store_true", help="Verbose mode for logging")
args = parser.parse_args()

with open('Datasets/'+args.n, 'r') as csvfile:
	temp = csvfile.read()
	lines = temp.split('\n')
	if args.v:
		print "csv lines: "+str(len(lines))
csvfile.close()

texts = []

for i in range(1,len(lines)): # we skip the first line with column headings
	data = lines[i].split(',')
	if len(data)>1:
		t = RedditText(data[0],data[1],sanitize(data[2]),data[3],data[4],sanitize(data[5]),sanitize(data[6]),sanitize(data[7]))
		texts.append(t)
if args.v:
	print "texts created: "+str(len(texts))

graphName = (args.n).split('.')[0]
f = open("Graphs/"+graphName+".graphml", "w")
writeHeader(f)

counter_texts = 0
counter_authors = 0
authors = []
edgeId = 0
counter_attackEdges = 0
counter_defenseEdges = 0
textWithReplies = []

for t in texts:
	# Node for text
	writeNode(f,'t_'+str(t.id),t.authorId,t.text,'text','blue',t.score,'','') # file, nodeId->text id, content->text text, nodeType->text, color->blue, score->reddit score (karma)
	counter_texts+=1

	# Node for author (if not already present)
	if t.authorId not in authors:
		writeNode(f,t.authorId,t.authorId,'','user','yellow',0,t.commentKarma,t.linkKarma) # file, nodeId->author id, authorId->'user name', content->'', nodeType->user, color->yellow, score->0 (for users), commentKarma, linkKarma
		counter_authors+=1
		authors.append(t.authorId)

	# Edge author->text [AUTHORSHIP]
	writeEdge(f,'e_'+str(edgeId),1,'authorship','blue',t.authorId,'t_'+str(t.id)) # file, edgeId->edgeId counter, weight, edgeType, color, source, target
	edgeId+=1

	if t.hasReplies=='True':
		textWithReplies.append([t.id,t.repliesTo])
		# Edge text->text [ATTACK]
		writeEdge(f,'e_'+str(edgeId),1,'attack','red','t_'+str(t.id),'t_'+str(t.repliesTo)) # file, edgeId->edgeId counter, weight, edgeType, color, source, target
		counter_attackEdges+=1
		edgeId+=1

		for tr in textWithReplies:
			if t.repliesTo==tr[0] and t.repliesTo!=tr[1]: # we check if the defended text is NOT from the same author of the currently attacked texts.
				# Edge text->text [DEFENSE]
				writeEdge(f,'e_'+str(edgeId),1,'defense','green','t_'+str(t.id),'t_'+str(tr[1])) # file, edgeId->edgeId counter, weight, edgeType, color, source, target
				counter_defenseEdges+=1
				edgeId+=1



if args.v:
	print "text nodes created: "+str(counter_texts)
	print "author nodes created: "+str(counter_authors)
	print "attack edges created: "+str(counter_attackEdges)
	print "defense edges created: "+str(counter_defenseEdges)

writeFooter(f)
f.close()


