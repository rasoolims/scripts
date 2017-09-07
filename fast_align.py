import os,sys,codecs



def create_data(directory, src, dst, output):
	src_lines = codecs.open(directory+'corpus.tok.clean.lower.'+src,'r').read().strip().split('\n')
	dst_lines = codecs.open(directory+'corpus.tok.clean.lower.'+dst,'r').read().strip().split('\n')
	assert len(src_lines) == len(dst_lines)
	writer = codecs.open(output,'w')

	for i in xrange(len(src_lines)):
		writer.write(src_lines[i].strip()+' ||| '+dst_lines[i].strip()+'\n')
	writer.close()

def convert_format(inp_file, out_file, do_revert=False):# index starts from one
	lines = open(inp_file,'r').read().strip().split('\n')
	writer = open(out_file, 'w')
	for l in lines:
		spl = l.strip().split(' ')
		output = ['0-0']
		for s in spl:
			st = s.split('-')
			s = int(st[0])+1
			t = int(st[1])+1
			if do_revert:
				output.append(str(t)+'-'+str(s))
			else:
				output.append(str(s)+'-'+str(t))
		writer.write(' '.join(output)+'\n')
	writer.close()



if __name__ == "__main__":
	if len(sys.argv)<5:
		print 'directory script_dir src dst'
		sys.exit(0)

	directory = os.path.abspath(sys.argv[1])+'/'
	script_dir = os.path.abspath(sys.argv[2])+'/'
	src =  sys.argv[3]
	dst =  sys.argv[4]
	aligned_file = directory+'fastalign_input.txt'
	create_data(directory, src, dst,aligned_file)

	command = '/'+ script_dir+'word-aligner/fast_align  -i ' + aligned_file+ ' -d -o -v > ' + directory + 'forward.align'
	print command
	os.system(command)

	command = '/'+ script_dir+'word-aligner/fast_align  -i ' + aligned_file+ ' -d -o -v -r  > ' + directory + 'backward.align'
	print command
	os.system(command)

	command = '/'+ script_dir+'utils/atools  -i '+directory + 'forward.align -j '+ directory + 'backward.align -c grow-diag-final > ' + directory + 'grow_diag.fastalign'
	print command
	os.system(command)

	convert_format( directory + 'grow_diag.fastalign', directory+src+'2'+dst+'.grow.fastalign')
	convert_format( directory + 'grow_diag.fastalign', directory+dst+'2'+src+'.grow.fastalign',True)

