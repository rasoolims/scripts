import os,sys

if len(sys.argv)<5:
	print 'args: [bible_folder] [l1] [l2] [cdec script_dir]'
	sys.exit(0)

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

giza2align = os.path.dirname(os.path.abspath(sys.argv[0]))+'/gizaA3_to_fast_align.py'
bible_folder = os.path.abspath(sys.argv[1])+'/'
l1, l2 = sys.argv[2], sys.argv[3]
script_dir = os.path.abspath(sys.argv[4])+'/'

src_align = bible_folder + l1+'_'+l2 + '.giza.forward.align'
dst_align = bible_folder + l2+'_'+l1 + '.giza.backward.align'
grow_diag_file = bible_folder + 'grow_diag.fastalign' 

command = 'python -u ' + giza2align + ' ' + bible_folder + l1+'_'+l2+'.align.A3.final '+ src_align + ' & '
print command
os.system(command)

command = 'python -u ' + giza2align + ' ' + bible_folder + l2+'_'+l1+'.align.A3.final '+ dst_align + ' flip'
print command
os.system(command)

command = '/'+ script_dir+'utils/atools  -i '+ src_align +' -j '+ dst_align +' -c grow-diag-final > ' + grow_diag_file
print command
os.system(command)

print 'converting'
convert_format(grow_diag_file, bible_folder+l1+'2'+l2+'.grow.giza')
convert_format(grow_diag_file, bible_folder+l2+'2'+l1+'.grow.giza',True)
print 'done with', bible_folder