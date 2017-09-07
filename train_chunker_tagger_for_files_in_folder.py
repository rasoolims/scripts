import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<9:
	print 'code_folder train_tag_folder dev_tag_folder  train_folder dev_folder embedding_folder model_folder langs(separated by ,)'
	sys.exit(0)
remover =os.path.dirname(os.path.realpath(__file__))+'/remove_syntax_from_chunk.py'

code_folder = os.path.abspath(sys.argv[1])+'/'
train_tag_folder = os.path.abspath(sys.argv[2])+'/'
dev_tag_folder = os.path.abspath(sys.argv[3])+'/'
train_folder = os.path.abspath(sys.argv[4])+'/'
dev_folder = os.path.abspath(sys.argv[5])+'/'
embedding_folder = os.path.abspath(sys.argv[6])+'/'
model_folder = os.path.abspath(sys.argv[7])+'/'
langs= sys.argv[8].split(',')


if not os.path.isdir(model_folder): os.mkdir(model_folder)

print os.listdir(train_folder)
commands = list()
for f in langs:
	if not os.path.isdir(model_folder+f): os.mkdir(model_folder+f)
	print 'train pos tagger for',f
	if not os.path.isdir(model_folder+f+'/pos'): os.mkdir(model_folder+f+'/pos')
	command = 'python -u ' + code_folder+ 'src/postagger.py --train '+ train_tag_folder+f +' --dev '+dev_tag_folder+f+' --outdir  '+ model_folder+f+'/pos/ --save_best --epochs 20 --init '+ embedding_folder+f+'.gz --wembedding 100 --mem 10024'
	print command
	os.system(command)

for f in langs:
	print 'train chunker for',f
	if not os.path.isdir(model_folder+f+'/chunk'): os.mkdir(model_folder+f+'/chunk')
	command = 'python -u '+code_folder+ 'src/bilstmtagger.py --train '+ train_folder+f +' --dev '+dev_folder+f +' --outdir '+ model_folder+f+'/chunk/ --save_best --epochs 20 --tag_init  --wembedding 100 --batch 50 --pos_model '+model_folder+f+'/pos/model.model --pos_params '+model_folder+f+'/pos/params.pickle --k 3 --mem 40024'
	print command
	os.system(command)

	print 'chunk with the final model',f
	command = 'python -u '+code_folder+ 'src/bilstmtagger.py --test '+ dev_folder+f +' --outfile '+model_folder+f +'/dev.out --model '+model_folder+f+'/chunk/model.model --params '+ model_folder+f+'/chunk/params.pickle --pos_model '+model_folder+f+'/pos/model.model --pos_params '+model_folder+f+'/pos/params.pickle --mem 40024 --eval'
	print command
	os.system(command)

	command = 'python -u '+ remover+' ' +model_folder+f +'/dev.out ' +model_folder+f +'/dev_no_syn.out'
	print command
	os.system(command)
print 'done!'



