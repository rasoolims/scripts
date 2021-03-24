import os
import sys

with open(os.path.abspath(sys.argv[1]), "r") as reader, open(os.path.abspath(sys.argv[2]), "w") as writer:
	for line in reader:
		line = line.strip()
		if line.startswith("# text ="):
			line = line[8:].strip()
			writer.write(line+"\n")

