import os
import sys


en_path = os.path.abspath(sys.argv[1])
en_moses_path = os.path.abspath(sys.argv[2])
en_tok_path = os.path.abspath(sys.argv[3])
foreign_path = os.path.abspath(sys.argv[4])
en_foreign_path = os.path.abspath(sys.argv[5])
foreign_tok_path = os.path.abspath(sys.argv[6])
en_other_fastalign =  os.path.abspath(sys.argv[7])
other_tokenized =  os.path.abspath(sys.argv[8])
output_file_source =  os.path.abspath(sys.argv[9])
output_file_target =  os.path.abspath(sys.argv[10])

en_raw2tok = {}
en_moses2raw = {}

with open(en_path, "r") as en_reader, open(en_tok_path, "r") as en_tok_reader, open(en_moses_path, "r") as en_moses_reader:
	for line, tok_line, moses_line in zip(en_reader, en_tok_reader, en_moses_reader):
		en_raw2tok[line.strip()] = tok_line.strip()
		en_moses2raw[moses_line.strip()] = tok_line.strip()

print(len(en_raw2tok), len(en_moses2raw))



raw_foreign_sens = []
tok_foreign_sens = []
en_equiv_sens = []
missed_tokenized = 0

en2foreign_tok = {}

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
			en2foreign_tok[en_equiv_sens[len(tok_foreign_sens)]] = fl
			tok_foreign_sens.append(fl)


print(len(tok_foreign_sens))

assert len(raw_foreign_sens) == len(tok_foreign_sens)
print("missed tokenized", missed_tokenized)



en_to_translate = []
translations = []
translations_tok = []

with open(en_other_fastalign, "r") as en_other_fastalign_reader:
	for efl in en_other_fastalign_reader:
		spl = efl.strip().split(" ||| ")
		if len(spl)<2:
			continue
		src, dst = spl[0].strip(), spl[1].strip()

		if len(dst.strip())>0:
			en_to_translate.append(src)
			translations.append(dst)

print(len(translations))

with open(other_tokenized, "r") as other_tokenized_reader:
	for fl in other_tokenized_reader:
		fl = fl.strip()
		if len(fl)>0:
			translations_tok.append(fl)

print(len(translations_tok))
assert len(translations) == len(translations_tok)

written = 0
with open(output_file_source, "w") as source_writer, open(output_file_target, "w") as target_writer:
	for i, en_sen in enumerate(en_to_translate):
		en_tok_sen = en_moses2raw[en_sen] if en_sen in en_moses2raw else en_sen
		translation = translations_tok[i]
		if en_tok_sen in en2foreign_tok:
			source_writer.write(en2foreign_tok[en_tok_sen] + "\n")
			target_writer.write(translation + "\n")
			written += 1
print("written", written, "parallel sentences!")




