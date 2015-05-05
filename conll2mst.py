#! /usr/bin/python

import sys;

# Open File
f = open(sys.argv[1],'rt');

wrds = ""; pos = ""; labs = ""; par = "";

for line in f:
    
    sent = line.strip().split('\t');

    if len(sent) > 1:
        #if len(sent)<8:
            #print sent
        wrds += sent[1] + "\t";
        pos += sent[3] + "\t";
        labs += sent[7] + "\t";
        par += sent[6] + "\t";
    else:
        print wrds; wrds = "";
        print pos; pos = "";
        print labs; labs = "";
        print par; par = "";
        print "";

f.close();


