import os,sys,codecs,re


reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

line=reader.readline()

while line:
	output=re.sub('\(.*?\)','',line.strip())
	output=output.replace('  ',' ').replace('  ',' ').replace('  ',' ').strip()
	output=re.sub('\[.*?\]','',output)
	output=output.replace('  ',' ').replace('  ',' ').replace('  ',' ').strip()
	writer.write(output+'\n')
	line=reader.readline()
writer.flush()
writer.close()