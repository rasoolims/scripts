import os
import sys


en_path = os.path.abspath(sys.argv[1])
en_tok_path = os.path.abspath(sys.argv[2])
foreign_path = os.path.abspath(sys.argv[3])
en_foreign_path = os.path.abspath(sys.argv[4])
foreign_tok_path = os.path.abspath(sys.argv[5])

en_raw2tok = {}

with open(en_path, "r") as en_reader, open(en_tok_path, "r") as en_tok_reader:
	for line, tok_line in zip(en_reader, en_tok_reader):
		en_raw2tok[line.strip()] = tok_line.strip()
print(len(en_raw2tok))



raw_foreign_sens = []
tok_foreign_sens = []
en_equiv_sens = []
missed_tokenized = 0

with open(foreign_path, "r") as foreign_reader, open(en_foreign_path, "r") as en_foreign_reader:
	for fl, el in zip(foreign_reader, en_foreign_reader):
		fl = fl.strip()
		if len(fl)>0:
			raw_foreign_sens.append(fl)
			el = el.strip()
			if el in en_raw2tok:
				en_equiv_sens.append(en_raw2tok[el])
			else:
				en_equiv_sens.append(el)
				missed_tokenized += 1


print(len(raw_foreign_sens))

with open(foreign_tok_path, "r") as foreign_tok_reader:
	for fl in foreign_tok_reader:
		fl = fl.strip()
		if len(fl)>0:
			tok_foreign_sens.append(fl)

print(len(tok_foreign_sens))

assert len(raw_foreign_sens) == len(tok_foreign_sens)
print("missed tokenized", missed_tokenized)

