import os
import sys


en_path = os.path.abspath(sys.argv[1])
en_moses_path = os.path.abspath(sys.argv[2])
en_tok_path = os.path.abspath(sys.argv[3])
foreign_path = os.path.abspath(sys.argv[4])
en_foreign_path = os.path.abspath(sys.argv[5])
foreign_tok_path = os.path.abspath(sys.argv[6])


en_raw2tok = {}
en_moses2raw = {}

with open(en_path, "r") as en_reader, open(en_tok_path, "r") as en_tok_reader, open(en_moses_path, "r") as en_moses_reader:
	for line, tok_line, moses_line in zip(en_reader, en_tok_reader, en_moses_reader):
		en_raw2tok[line.strip()] = tok_line.strip()
		en_moses2raw[moses_line.strip()] = line.strip()

print(len(en_raw2tok), len(en_moses2raw))



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

