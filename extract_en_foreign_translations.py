import os
import sys


en_path = os.path.abspath(sys.argv[1])
en_moses_path = os.path.abspath(sys.argv[2])
en_tok_path = os.path.abspath(sys.argv[3])

en_other_fastalign =  os.path.abspath(sys.argv[4])
other_tokenized =  os.path.abspath(sys.argv[5])
output_file_source =  os.path.abspath(sys.argv[6])
output_file_target =  os.path.abspath(sys.argv[7])

en_raw2tok = {}
en_moses2raw = {}

with open(en_path, "r") as en_reader, open(en_tok_path, "r") as en_tok_reader, open(en_moses_path, "r") as en_moses_reader:
	for line, tok_line, moses_line in zip(en_reader, en_tok_reader, en_moses_reader):
		en_raw2tok[line.strip()] = tok_line.strip()
		en_moses2raw[moses_line.strip()] = tok_line.strip()

print(len(en_raw2tok), len(en_moses2raw))





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
		source_writer.write(en_tok_sen + "\n")
		target_writer.write(translation + "\n")
		written += 1
print("written", written, "parallel sentences!")




