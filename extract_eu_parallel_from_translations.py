import os
import sys


en_path = os.path.abspath(sys.argv[1])
en_tok_path = os.path.abspath(sys.argv[2])

en_raw2tok = {}

with open(en_path, "r") as en_reader, open(en_tok_path, "r") as en_tok_reader:
	for line, tok_line in zip(en_reader, en_tok_reader):
		en_raw2tok[line.strip()] = tok_line.strip()
print(len(en_raw2tok))

