import os,sys,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf-8')

line=reader.readline()
while line:
	spl=line.strip().split(' ')
	if spl[0]!='#':
		suf=''
		word=''
		stem=''

		is_suf=True
		for i in range(len(spl)-1,0,-1):
			morph=spl[i][:spl[i].rfind('/')]
			word=morph+word
			if not is_suf:
				stem=morph+stem
			elif is_suf and spl[i].endswith('/SUF'):
				suf=morph+suf
			else:
				is_suf=False
				stem=morph+stem
		if word!=stem and not stem.endswith('-'):
			writer.write(word+u'\t'+stem+u'\n')


	line=reader.readline()
writer.flush()
writer.close()