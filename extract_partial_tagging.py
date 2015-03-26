import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<4:
	print 'python extract_partial_tagging.py [min_ratio] [min_len] [input_file] [output_file] [only_partial: true or false (optional)]'
	sys.exit(0)


def has_condition(sen,min_ratio,min_len,only_partial):
	spl=sen.split(' ')

	length=len(spl)
	r=0
	stretch=0
	max_stretch=0

	for s in spl:
		if not s.endswith('_***'):
			r+=1
			stretch+=1
		else:
			if stretch>max_stretch:
				max_stretch=stretch
			stretch=0
	if stretch>max_stretch:
		max_stretch=stretch

	ratio=float(r)/length

	if only_partial and r==length:
		return False
	if r==length or ratio>=min_ratio or max_stretch>=min_len:
		return True

	return False



min_ratio=float(sys.argv[1])
min_len=int(sys.argv[2])

reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
writer=codecs.open(os.path.abspath(sys.argv[4]),'w')

only_partial=False
if len(sys.argv)>5 and sys.argv[5]=='true':
	only_partial=True

line=reader.readline()
while line:
	line=line.strip()

	if has_condition(line,min_ratio,min_len,only_partial):
		writer.write(line+'\n')

	line=reader.readline()

writer.flush()
writer.close()
