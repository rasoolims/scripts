import os
import sys
from string import printable


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
			word = ''.join(char for char in spl[0] if char in printable)
			words.append(word.replace("|", ""))

	if len(words)>0:
		raw2conllu[" ".join(words)] = sen

print(len(raw2conllu))

with open(raw_path, "r") as reader, open(output_path, "w") as writer:
	for line in reader:
		sen = line.strip()
		sen = ''.join(char for char in sen if char in printable)

		assert sen in raw2conllu, sen +" =>> " + conllu_path

		writer.write(raw2conllu[sen]+"\n\n")

print("Done!")