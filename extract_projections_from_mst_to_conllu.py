import os
import sys

none_filter = lambda x: filter(lambda x: x is not None, x)

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


print("MST trees loading done with {0} trees!".format(len(sentence_trees)))


print("Loading Conllu trees!")

conllu_trees = open(os.path.abspath(sys.argv[2]), "r").read().strip().split("\n\n")
print("Conllu trees loading done with {0} trees!".format(len(conllu_trees)))

with open(os.path.abspath(sys.argv[3]), "w") as writer:
    found = 0
    for ti, tree in enumerate(conllu_trees):
        lines = tree.strip().split("\n")
        word_and_ids = list(map(lambda line: line.strip().split("\t")[:2], lines))
        sen = " ".join(none_filter(map(lambda word_id: word_id[1] if word_id[0].isdigit() else None, word_and_ids)))

        if sen in sentence_trees:
            found +=1
            output = []
            labels, relations = sentence_trees[sen]

            for line in lines:
                spl = line.strip().split("\t")
                if spl[0].isdigit():
                    wid = int(spl[0])-1
                    rel = relations[wid]
                    dep_labl = labels[wid]

                    spl[6] = rel
                    spl[7] = dep_labl if int(rel)!=-1 else "_"
                writer.write("\t".join(spl))
                writer.write("\n")
            writer.write("\n")

        if ti%10000==0:
            print(ti, "found:", found, end="\r")

print("{0} Conllu trees found in MST trees!".format(found))


