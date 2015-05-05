import os,sys,codecs

## extracts parallel data from Korean bilingual corpus
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')

writer1=codecs.open(os.path.abspath(sys.argv[2])+'.en','w')
writer2=codecs.open(os.path.abspath(sys.argv[2])+'.ko','w')

line=reader.readline()
count=0
while line:
	line=line.strip()

	if line.startswith('#'):
		
		eline=line[1:]
		kline=reader.readline().strip()
		if kline.startswith('#'):
			kline=kline[1:]


		if eline and kline:
			if  is_ascii(eline):
				writer1.write(eline+'\n')
				writer2.write(kline+'\n')

	line=reader.readline()

writer1.flush()
writer1.close()
writer2.flush()
writer2.close()