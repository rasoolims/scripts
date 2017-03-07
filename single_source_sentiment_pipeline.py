import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<9:
	print 'senti_script_path eval_script_path data_folder embedding_file cluster_file output_folder target_langs(separated by,) use_english(true or false) test_folder'
	sys.exit(0)

senti_script_path = os.path.abspath(sys.argv[1])
eval_script_path = os.path.abspath(sys.argv[2])
data_folder = os.path.abspath(sys.argv[3])+'/'
embedding_file = os.path.abspath(sys.argv[4])
cluster_file = os.path.abspath(sys.argv[5])
output_folder = os.path.abspath(sys.argv[6])+'/'
target_langs = sys.argv[7].strip().split(',')
use_english = True if sys.argv[8]=='true' else False
test_folder = os.path.abspath(sys.argv[9])+'/'

print target_langs

for f in os.listdir(data_folder):
	l1,l2 = f.split('2')[0],f.split('2')[1]

	if l2 in target_langs and (use_english or l1 != 'en'):
		if not os.path.isdir(output_folder+f): os.mkdir(output_folder+f)
		command = 'nice python -u ' + senti_script_path  +' --train '+data_folder+f+' --outdir '+output_folder+f+' --embed_dim 400 --hidden 400 --lstmdims 400 --activation relu --embed '+embedding_file+' --dropout 0 --cluster '+ cluster_file+' --epochs 7 --batch 10000  --pool'
		print command
		os.system(command)

		command = 'nice python -u ' + senti_script_path  + ' --input '+test_folder+l2 + ' --output '+output_folder+f+'/test.out --model '+output_folder+f+'/model.model.final --params '+output_folder+f+'/params.pickle '

		print command
		os.system(command)


		command = ' nice python -u '+ eval_script_path +' '+ test_folder+l2 +' '+output_folder+f+'/test.out > '+output_folder+f+'/eval.out'
		print command
		os.system(command)

		command = 'gzip '+output_folder+f+'/* &'
		print command
		os.system(command)
