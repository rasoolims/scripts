import os,sys,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

count=0
line=reader.readline()
while line:
    spl=line.strip().split(' ')
    if spl[1]=='<?>':
        spl[1]='*UNKNOWN*'
    writer.write(' '.join(spl[1:])+'\n')
    count+=1
    if count%1000000==0:
        sys.stdout.write(str(count/1000000)+'M...')
    line=reader.readline()

sys.stdout.write(str(count)+'\n')
writer.close()