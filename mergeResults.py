#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join

resultsFiles = [f for f in listdir("Results/") if isfile(join("Results/", f))]

with open('mergedResults.csv', 'w') as outfile:
    outfile.write("ConversationID,User,Tweets,Atk_IN,Atk_OUT,Def_IN,Def_OUT,M0,M1,M2,M3,M4,M5,M6,Engagement,X_Engagement,Global Score,Norm. GS,D,inD,outD,E,C,B,D-T,inD-T,outD-T,E-T,C-T,B-T,RS,C-Karma,L-Karma\n")
    for fname in resultsFiles:
        arg_name=fname.split(".")[0]
        with open("Results/"+fname) as infile:
            i=0
            for line in infile:
                if i>1:
                    tempLine=line.replace("\t",",")
                    outfile.write(arg_name+","+tempLine)
                i+=1