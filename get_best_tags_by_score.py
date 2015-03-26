import sys,os,codecs,operator

tags=dict()

if len(sys.argv)<4:
	print 'python get_best_tags_by_score.py [input_tagged_file] [score_file] [max_num] [output_file]'
	sys.exit(0)

max_tag=int(sys.argv[3])
writer=codecs.open(os.path.abspath(sys.argv[4]),'w')

print 'reading tags...'
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		tags[line_count]=line
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
	line=reader.readline()

reader=codecs.open(os.path.abspath(sys.argv[2]),'r')

scores=dict()
line_count=0

print '\nreading scores...'
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		scores[line_count]=float(line)
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
	line=reader.readline()

print '\nsorting scores...'
sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)

i=0
print 'writing trees...'

for s in sorted_scores:
	i+=1
	if i>max_tag:
		break

	index=s[0]
	writer.write(tags[index]+'\n\n')

writer.flush()
writer.close()



