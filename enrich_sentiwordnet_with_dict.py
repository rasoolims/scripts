import os,sys,codecs

print '[dict_file] [en_senti] [output]'
en2l_dict = {line.strip().split()[0]:line.strip().split()[1] for line in codecs.open(os.path.abspath(sys.argv[1]),'r')}

writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	writer.write(line.strip()+'\n')
	word,pos,neg = line.strip().split()
	if word in en2l_dict:
		writer.write(en2l_dict[word]+'\t'+pos+'\t'+neg+'\n')
writer.close()