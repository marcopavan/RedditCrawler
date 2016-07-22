#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sanitize(t):
	chars_to_remove = ['<','>','=','\r','\n']
	t=t.encode('utf-8').translate(None,''.join(chars_to_remove))
	t=t.replace('&','and').replace(',',' ').replace("\u2018", "'").replace("\u2019", "'")
	t=remove_non_ascii_char(t)
	return t

def replyId_cleaner(replyId):
    return str(replyId.split('_')[1])

def remove_non_ascii_char(text):
    return ''.join(i for i in text if ord(i)<128)

def printTime(startTime, endTime):
        t = endTime - startTime
        if t > 60000:                         	# more than 1 minute
            temp = round(t / float(1000), 1)
            m = int(temp / float(60))
            s = str(temp - (m * 60))
            print "Time: " + str(int(m)) + " m. " + s + " s."
        elif t > 1000:                        	# more than 1 second
            s = str(round(t / float(1000), 1))
            print "Time: " + s + " s."
        else:                               	# less than 1 second
            print "Time: " + str(t) + " ms."

##### ##### #####

def writeHeader(f):
	f.write(
		"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- This file was written with python.-->\n<graphml xmlns=\""
		"http://graphml.graphdrawing.org/xmlns\"  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
		"\nxsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/"
		"graphml.xsd\">\n")

	f.write("<key id=\"n0\" for=\"node\" attr.name=\"author\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n1\" for=\"node\" attr.name=\"content\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n2\" for=\"node\" attr.name=\"nodeType\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n3\" for=\"node\" attr.name=\"color\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n4\" for=\"node\" attr.name=\"score\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n5\" for=\"node\" attr.name=\"commentKarma\" attr.type=\"string\"/>\n")
	f.write("<key id=\"n6\" for=\"node\" attr.name=\"linkKarma\" attr.type=\"string\"/>\n")

	f.write("<key id=\"e0\" for=\"edge\" attr.name=\"weight\" attr.type=\"float\"/>\n")
	f.write("<key id=\"e1\" for=\"edge\" attr.name=\"edgeType\" attr.type=\"string\"/>\n")
	f.write("<key id=\"e2\" for=\"edge\" attr.name=\"color\" attr.type=\"string\"/>\n")

	f.write("<graph id=\"G\" edgedefault=\"directed\">\n")

def writeNode(f,i,author,content,nodeType,color,score,commentKarma,linkKarma):
	f.write("\t<node id=\""+str(i)+"\">\n")
	f.write("\t\t<data key=\"n0\">"+str(author)+"</data>\n")
	f.write("\t\t<data key=\"n1\">"+str(content)+"</data>\n")
	f.write("\t\t<data key=\"n2\">"+str(nodeType)+"</data>\n")
	f.write("\t\t<data key=\"n3\">"+str(color)+"</data>\n")
	f.write("\t\t<data key=\"n4\">"+str(score)+"</data>\n")
	f.write("\t\t<data key=\"n5\">"+str(commentKarma)+"</data>\n")
	f.write("\t\t<data key=\"n6\">"+str(linkKarma)+"</data>\n")
	f.write("\t</node>\n")

def writeEdge(f,i,weight,edgeType,color,source,target):
	f.write("\t<edge id=\""+str(i)+"\" source=\""+str(source)+"\" target=\""+str(target)+"\">\n")
	f.write("\t\t"+"<data key=\"e0\">"+str(weight)+"</data>\n")
	f.write("\t\t"+"<data key=\"e1\">"+str(edgeType)+"</data>\n")
	f.write("\t\t"+"<data key=\"e2\">"+str(color)+"</data>\n")
	f.write("\t</edge>\n")

def writeFooter(f):
	 f.write("</graph>\n</graphml>")

##### ##### #####

def checkAuthors(a,replies,texts):
	authorA=""
	authorB=""
	for t in texts:
		if t.id==a:
			authorA = t.authorId
		for r in replies:
			if t.id==r:
				authorB = t.authorId
	if authorA!=authorB:
		return True
	else:
		return False

##### ##### #####

def polarize(score):
	if score>0:
		return 1
	elif score<0:
		return -1
	else:
		return 0