import os
import sys

with open(os.path.abspath(sys.argv[1]), "r") as reader, open(os.path.abspath(sys.argv[2]), "w") as writer:
	words = []
	for line in reader:
		line = line.strip()
		if len(line) == 0 and len(words)>0:
			writer.write(" ".join(words)+"\n")
			words = []

		spl = line.split("\t")
		if spl[0].isdigit():
			words.append(spl[1].strip())
	if len(words)>0:
		writer.write(" ".join(words)+"\n")
