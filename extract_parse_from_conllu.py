import os
import sys

def empty_tree(sen):
	words = sen.strip().split(" ")

	output = []
	for i, w in enumerate(words):
		o = [str(i+1), w, w] + ["_"]*8
		output.append("\t".join(o))
	return "\n".join(output)


conllu_path = os.path.abspath(sys.argv[1])
raw_path = os.path.abspath(sys.argv[2])
output_path = os.path.abspath(sys.argv[3])

conllu_data = open(conllu_path, "r").read().strip().split("\n\n")
raw2conllu = {}
for sen in conllu_data:
	sen = sen.strip()
	lines = sen.split("\n")
	words = []

	for line in lines:
		spl = line.strip().split("\t")
		if spl[0].isdigit():
			words.append(spl[1].replace("|", ""))

	if len(words)>0:
		raw2conllu[" ".join(words)] = sen

print(len(raw2conllu))

with open(raw_path, "r") as reader, open(output_path, "w") as writer:
	for line in reader:
		sen = line.strip()
		if sen not in raw2conllu:
			empty_tree_str = empty_tree(sen)
			writer.write(empty_tree_str+"\n\n")
			print("EROOR:", sen +" =>> " + conllu_path)
			print(empty_tree_str)
		else:
			writer.write(raw2conllu[sen]+"\n\n")

print("Done!")