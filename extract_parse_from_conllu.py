import os
import sys


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
			words.append(spl[1])

	if len(words)>0:
		raw2conllu[" ".join(words)] = sen

print(len(raw2conllu))