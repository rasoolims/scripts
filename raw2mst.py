import os,sys,math,re,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

line=reader.readline()
while line:
    line=re.sub(r'\s+', ' ', line.strip())
    if line:
        words=line.split(' ')
        lenw=len(words)
        heads=['-1']*lenw
        labels=['_']*lenw
        tags=['_']*lenw

        writer.write('\t'.join(words)+'\n')
        writer.write('\t'.join(tags)+'\n')
        writer.write('\t'.join(labels)+'\n')
        writer.write('\t'.join(heads)+'\n\n')
    line=reader.readline()
writer.flush()
writer.close()