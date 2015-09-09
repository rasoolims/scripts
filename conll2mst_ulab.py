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
        par += sent[6] + "\t";
    else:
        if wrds.strip():
            print wrds; wrds = "";
            print pos; pos = "";
            print par; par = "";
            print "";
        else:
            wrds = "";
            pos = "";
            par = "";

f.close();


