import sys,codecs,os

reader = codecs.open(os.path.abspath(sys.argv[1]),'r')

num_lines = 0
num_tokens = 0
types = set()

line = reader.readline()
while line:
	line = line.strip()
	if line:
		spl = line.split()
		num_lines +=1
		num_tokens += len(spl)
		types |= set(spl)
	line = reader.readline()

print '#sentence',num_lines
print '#tokens',num_tokens
print '#types',len(types)
