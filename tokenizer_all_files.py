import os,sys,codecs
from collections import defaultdict
from os import listdir
from os.path import isfile, join
import glob

files = glob.glob(os.path.abspath(sys.argv[1])+"/*.*")
tokenizer_script_path=os.path.abspath(sys.argv[2])

for f in files:
	if 'tok.' in f:
		continue
	t = f[-2:]
	new_file = f[:-2]+'tok.'+t
	print '***********************************************************************'
	print f
	print new_file
	if t!='ko' and t!='ja':
		os.system('perl '+tokenizer_script_path+' -l '+t+' < '+ f +' > '+new_file )

print 'done!'