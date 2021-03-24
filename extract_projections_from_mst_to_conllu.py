import os
import sys


print("Loading MST trees!")
sentence_trees = {}
with open(os.path.abspath(sys.argv[1]), "r") as mst_reader:
    sentence = []
    for line in mst_reader:
        if len(line.strip()) == 0 and len(sentence)>0:
            words = " ".join(sentence[0])
            labels = sentence[2]
            relations = sentence[3]
            sentence_trees[words] = (labels, relations)
            sentence = []
        else:
            sentence.append(line.strip().split("\t")) 


print("MST trees loading done with {1} trees!".format(len(sentence_trees)))

