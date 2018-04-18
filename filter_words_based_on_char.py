import os,sys,codecs

reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv)<4:
	print 'ref_char_file input_file output_file'

all_chars = set()
for line in codecs.open(os.path.abspath(sys.argv[1]), 'r'):
	for c in list(line.strip().lower()):
		if c.strip():
			all_chars.add(c.strip())

print 'number of chars', len(all_chars)

all_words, kept = 0, 0
writer = codecs.open(os.path.abspath(sys.argv[3]), 'w')
for line in codecs.open(os.path.abspath(sys.argv[2]), 'r'):
	output = []
	for word in line.strip().lower().split():
		all_words += 1
		is_good = True
		for c in list(word):
			if not c in all_chars:
				is_good = False
				break
		if is_good:
			output.append(word)
			kept += 1
	writer.write(' '.join(output)+'\n')
writer.close()
print kept, all_words



