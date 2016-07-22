#!/usr/bin/python
# -*- coding: utf-8 -*-

# USAGE EXAMPLE:
# python main.py -n test100 -f -v
# python main.py -n 4ogcwa -f -v
# python main.py -n hot -f -v
# python main.py -n hot -l 5 -f -v

import argparse
import os
from os import listdir
from os.path import isfile, join
import time
from functions import printTime

parser = argparse.ArgumentParser(description='Debug')
parser.add_argument("-n", required=True, help="Insert conversation ID to analyze (ex: 4ogcwa) or conversation keyword to analyze a set (ex: hot)")
parser.add_argument("-l", default="1", help="Limit the number of retrieved conversations (only used with conversation keywords like 'hot' or 'top')")
parser.add_argument("-v", action="store_true", help="Verbose mode for logging")
parser.add_argument("-f", action="store_true", help="Print results on file")
args = parser.parse_args()

start_tot_time = int(round(time.time() * 1000))

# Datasets
reddit_conversations_code_trainingset = ['4owlek','4lvntk','4ns33w','4nr0h4','4o500n','4osrq7','4kxii8','4lxlks','4p8520','4nplqm','4l3tik','4l0g42','4l4pcw','4opz6y','4npun5','4l0loc','4nrsyb','4ltncq','4ohufh','4l3h64','4ou8ct','4maowg','4ny59k','4oxe50','4mny2f','4n8hh7','4mgtca','4na57y','4nz84c','4p46uv','4nbd3b','4l5vmq','4ngag2','4mentx','4nrmcw','4lq3lo','4m7lij','4nsisd','4oijum','4p5jil','4osh6q','4p4wuc','4ox9w5','4nql8f','4ob3lw','4nkri8','4o5rel','4oxg9z','4n5d1f','4nxx8s','4mzewb','4n86se','4ly3vc','4lqt36','4ozqk9','4lrmbv','4mj34q','4m3zqy','4lbjwa','4ko3jy','4nqaik','4np3ao','4m7xdt','4o9x62','4niyw3','4ko4ud','4np6wq','4nsdas','4me06l','4my8g1','4nums0','4ldir5','4noord','4nooda','4npjly','4l3gx9','4nwhkq','4nsdhg','4noupz','4npqbx','4o8t8s','4nr1o8','4obv0l','4ncdut','4ng3z9','4mo10a','4nqidp','4nsbrj','4ns1nj','4ll529','4kvqml','4l2yep','4kyeqg','4m0eh4','4kvgp9','4omyqz','4mr5de','4nnhy7','4lvz4r','4ob02k','4o0gsm','4p0rh8','4l53y7','4m3mqe','4lkk87','4mpbbd','4nokok','4or2zx','4npywt','4nqspy','4mwp0i','4oizck','4matoo','4nw7sz','4nr9pl','4mv578','4nm65r','4nbkdp','4np2z1','4oz2t8','4l2hqc','4lq7yb','4lu3ux','4pbjzd','4lpria']

reddit_conversations_code_validationset =  ["4q2o6y","4ra3wr","4rrqjh","4qapql","4ru2mn","4qlg0b","4ruwjv","4qsgo4","4rizeu","4rc344","4qk71y","4q1a9a","4rpyaw","4pj3q3","4rtj3a","4rn2cs","4rkepj","4rb0pq","4rit3w","4qqon2","4qpnnp","4r9ld1","4rpoop","4puu41","4qh31e","4rip5u","4ppzvc","4p9qir","4nrboh","4pe4qf","4rj55j","4qabv3","4pogzj","4q0qe0","4rvoir","4q9lqy","4pn58q","4rw46t","4r3pcb","4qqffl","4rpj3l","4ptfdr","4qj6nu","4q2nlb","4qydte","4rtyjv","4qh5kg","4r3sww","4r9zpr","4r1zta","4q0om7","4nls7o","4rr3z0","4o3zy1","4rpqdv","4q8xeo","4phzsi","4phddu","4rf1jy","4oyvel","4rqwje","4rsbpj","4qa2am","4q896j","4q7d8q","4runc0","4rwbck","4p2hpl","4r4anr","4rvt4c","4q19oe","4ri3l6","4rkokk","4ros3w","4o11r2","4qh6fx","4osd7a","4pqku5","4nom6n","4rj5tt","4pzzov","4qfjms","4non9e","4nsz9w","4q5svb","4otqrm","4r30x8","4nr9nn","4rhysw","4nn7sm","4qe7sz","4p4656","4ph6hh","4nblqw","4psvcv","4rougw","4ruhw9","4pk6t5","4no2gz","4pmkpq"]


# Setting project folders
folders = ["Datasets/","Graphs/","Results"]

for f in folders:
    if not os.path.exists(f):
        os.makedirs(f)

# Crawling
if args.v:
    print "Fetching started..."

csvFiles = [f for f in listdir("Datasets/") if isfile(join("Datasets/", f))]

i=1
if args.n=='trainingset':
    if args.v:
        print "Retrieving comments from TEST submissions..."
    for conversation in reddit_conversations_code_trainingset:
        if not any(conversation in s for s in csvFiles):
            if args.v:
                print "Crawling conversation "+ str(conversation)+" ("+str(i)+"/"+str(len(reddit_conversations_code_trainingset))+")"
            os.system("python crawler.py -n " + str(conversation) + (" -v" if args.v else " "))
            if args.v:
                print "--- --- --- ---"
        else:
            print "CSV for "+conversation+" already built!"
        i+=1
if args.n=='validationset':
    if args.v:
        print "Retrieving comments from TEST submissions..."
    for conversation in reddit_conversations_code_validationset:
        if not any(conversation in s for s in csvFiles):
            if args.v:
                print "Crawling conversation "+ str(conversation)+" ("+str(i)+"/"+str(len(reddit_conversations_code_validationset))+")"
            os.system("python crawler.py -n " + str(conversation) + (" -v" if args.v else " "))
            if args.v:
                print "--- --- --- ---"
        else:
            print "CSV for "+conversation+" already built!"
        i+=1
elif args.n=='top':
    if args.v:
        print "Retrieving comments from top submissions..."
    os.system("python crawler.py -t" +" -l "+args.l+ (" -v" if args.v else " "))
    if args.v:
        print "--- --- --- ---"
elif args.n=='hot':
    if args.v:
        print "Retrieving comments from hot submissions..."
    os.system("python crawler.py -s" +" -l "+args.l+ (" -v" if args.v else " "))
    if args.v:
        print "--- --- --- ---"
else:
    if args.v:
        print "Retrieving comments from conversation with id "+str(args.n)+"..."
        os.system("python crawler.py -n " + str(args.n) + (" -v" if args.v else " "))
    if args.v:
        print "--- --- --- ---"

csvFiles = [f for f in listdir("Datasets/") if isfile(join("Datasets/", f))]
graphsFiles = [f for f in listdir("Graphs/") if isfile(join("Graphs/", f))]

# Building
if args.v:
    print "Building graphs..."

i=0
for f in csvFiles:
    if f.split('.')[1]=="csv":
        if not any(f.split('.')[0] in s for s in graphsFiles):
            if args.v:
                print "Building graph for "+f
            os.system("python graph_builder.py -n "+f+(" -v" if args.v else ""))
            if args.v:
                print "--- --- --- --- ---"
            i+=1
        else:
            print "Graph for "+f+" already built!"

if args.v:
    print str(i)+" graphs created."
    print "--- --- --- --- ---"

# Analyzing
if args.v:
    print "Analyzing graphs..."

graphsFiles = [f for f in listdir("Graphs/") if isfile(join("Graphs/", f))]
resultsFiles = [f for f in listdir("Results/") if isfile(join("Results/", f))]

if args.f and os.path.exists("Results/"+args.n+".txt"):
    os.remove("Results/"+args.n+".txt")

i=0
for f in graphsFiles:
    if f.split('.')[1]=="graphml":
        if not any(f.split('.')[0] in s for s in resultsFiles):
            if args.v:
                print "Analyzing graph "+f
            os.system("python graph_analyzer.py -n "+f+(" -v" if args.v else "")+(" -f -m w" if args.f else ""))
            if args.v:
                print "--- --- --- --- ---"
            i+=1
        else:
            print "Results for "+f+" already computed!"

if args.v:
    print str(i)+" graphs analyzed."
    print "--- --- --- --- ---"

# Merging results
if args.v:
    print "Merging results..."
os.system("python mergeResults.py")
if args.v:
    print "Merging completed."

end_tot_time = int(round(time.time() * 1000))

if args.v:
    printTime(start_tot_time, end_tot_time)