import os,sys,codecs,random

print '[uniq_parse_dir] [pos_map_file] [alignment_dir]'

my_path = os.path.abspath(os.path.dirname(sys.argv[0]))+'/'
uniq_parse_path = os.path.abspath(os.path.dirname(sys.argv[1]))+'/'
general_pos_path = os.path.abspath(sys.argv[2])

script1 = my_path+'get_alignment_intersection.py'
script2 = my_path+'create_dictionary_from_alignment.py'
script3 = my_path+'project_alignment.py'
parse_retiever = my_path+'parse_retriever.jar'
conll2mst = my_path + 'conll2mst.py'

#print my_path
d = os.path.abspath(sys.argv[3])+'/'
dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

for dr in dirs:
	i1 = dr.rfind('_')
	i2 = dr.rfind('/')
	l1 = dr[i2+1:i1]
	l2 = dr[i1+1:]

	align1 = dr +'/'+l1+'_'+l2+'.align.A3.final'
	align2 = dr +'/'+l2+'_'+l1+'.align.A3.final'
	intersect1 =  dr +'/'+l1+'2'+l2+'.intersect'
	intersect2 =  dr +'/'+l2+'2'+l1+'.intersect'
	raw_low1 =  dr +'/corpus.tok.clean.'+l1
	raw_low2 =  dr +'/corpus.tok.clean.'+l2
	raw1 =  dr +'/corpus.tok.clean.'+l1
	raw2 =  dr +'/corpus.tok.clean.'+l2
	conll1 =  dr +'/corpus.tok.clean.tag.conll.'+l1
	conll2 =  dr +'/corpus.tok.clean.tag.conll.'+l2
	mst1 =  dr +'/corpus.tok.clean.tag.mst.'+l1
	mst2 =  dr +'/corpus.tok.clean.tag.mst.'+l2
	dict1 =  dr +'/'+l1+'2'+l2+'.dict'
	dict2 =  dr +'/'+l2+'2'+l1+'.dict'
	project1 =  dr +'/'+l1+'2'+l2+'.project'
	project2 =  dr +'/'+l2+'2'+l1+'.project'
	uniq1 = uniq_parse_path+'corpus.tok.tag.yara.'+l1
	uniq2 = uniq_parse_path+'corpus.tok.tag.yara.'+l2

	# getting parse_files
	command1 = 'java -jar '+parse_retiever+' '+uniq1+' '+raw1+' '+conll1
	command2 =  'java -jar '+parse_retiever+' '+uniq2+' '+raw2+' '+conll2
	print command1
	os.system(command1)
	print command2
	os.system(command2)

	command1 = 'python '+conll2mst+' '+conll1 +' > '+mst1
	command2 = 'python '+conll2mst+' '+conll2 +' > '+mst2
	print command1
	os.system(command1)
	print command2
	os.system(command2)

	# getting intersection
	command1 = 'python -u '+script1 +' '+align1+' '+align2 + ' '+intersect1
	command2 = 'python -u '+script1 +' '+align2+' '+align1 + ' '+intersect2
	print command1
	os.system(command1)
	print command2
	os.system(command2)

	# getting alignment dict
	command1 = 'python -u '+script2 +' '+raw_low1 + ' '+raw_low2+' '+intersect1 +' '+dict1
	command2 = 'python -u '+script2 +' '+raw_low2 + ' '+raw_low1+' '+intersect2 +' '+dict2
	print command1
	os.system(command1)
	print command2
	os.system(command2)

	# gettting projection
	command1 = 'python -u '+script3 + ' '+mst1 +' '+mst2+' '+intersect1+' '+general_pos_path+' '+general_pos_path +' '+project1
	command2 = 'python -u '+script3 + ' '+mst2 +' '+mst1+' '+intersect2+' '+general_pos_path+' '+general_pos_path +' '+project2
	print command1
	os.system(command1)
	print command2
	os.system(command2)

print 'done!'
#nice python -u scripts/get_alignment_intersection.py experiments/alignment/qb/en_de/en_de.align.A3.final experiments/alignment/qb/en_de/de_en.align.A3.final experiments/alignment/qb/en_de/en2de.intersect

#nice python -u scripts/create_dictionary_from_alignment.py experiments/alignment/qb/en_de/corpus.tok.clean.lower.en experiments/alignment/qb/en_de/corpus.tok.clean.lower.de experiments/alignment/qb/en_de/en2de.intersect experiments/alignment/qb/en_de/en2de.dict