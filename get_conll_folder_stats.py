import os,sys,codecs

def get_stats(input_file):
	reader = codecs.open(input_file,'r')
	line =reader.readline()
	tok = 0
	sens=0
	types = set()
	start = True
	while line:
		spl = line.strip().split('\t')
		if len(spl)>7:
			if start:
				sens+=1
				start =False
			types.add(spl[1])
			tok+=1
		else:
			start = True
		line =reader.readline()
	return sens,tok,len(types)


input_folder = os.path.abspath(sys.argv[1])+'/'

print '| lang |   #sent.  |   #tok.  |   #type  |'
print '|------|:---------:|:--------:|:--------:|'
for f in os.listdir(input_folder):
	res= get_stats(input_folder+f)
	print '|  '+f+'  |    '+str(res[0])+'  |   '+str(res[1])+'   |   '+str(res[2])+'|'

