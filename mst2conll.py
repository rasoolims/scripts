#! /usr/bin/python

import sys;

# Open File
f = open(sys.argv[1],'rt');

wrds = "";
pos = "";
labs = "";
par = "";

for line in f:

    if len(line.strip()) == 0:
        if par=="":
            par=labs
            labs=""
        w = wrds.strip().split('\t'); p = pos.strip().split('\t'); l = labs.strip().split('\t'); pa = par.strip().split('\t');
        cnt = 1;
        for t in w:
            if len(labs.strip())>0:
                print str(cnt) + "\t" + t + "\t" + t + "\t" + p[cnt-1] + "\t" + p[cnt-1] + "\t_\t" + pa[cnt-1] + "\t" + l[cnt-1] +"\t_\t_";
            else:
                print str(cnt) + "\t" + t + "\t" + t + "\t" + p[cnt-1] + "\t" + p[cnt-1] + "\t_\t" + pa[cnt-1] + "\t_" +"\t_\t_" ;
            cnt += 1;
        print "";
        wrds = ""; pos = ""; labs = ""; par = "";
    elif len(wrds) == 0:
        wrds = line;
    elif len(pos) == 0:
        pos = line;
    elif len(labs) == 0:
        labs = line;
    else:
        par = line;

f.close();

