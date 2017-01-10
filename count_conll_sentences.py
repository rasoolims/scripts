import os,sys,codecs

sens = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
words = sum([len(s.strip().split('\n')) for s in sens])
print len(sens),words, float(words)/len(sens)
