import sys,codecs,os
from termcolor import colored

if len(sys.argv)<11:
	print colored('arguments: parser_path full_conll_path partial7_conll_path partial5_conll_path partial_all_conll_path model_dir iter1 iter2 iter3 iter4 embed_path','red')
	sys.exit(0)

print colored('reading arguments','red')
curr_dir=os.path.dirname(os.path.realpath(__file__))+'/'

parser_path=os.path.abspath(sys.argv[1])
full_conll_path=os.path.abspath(sys.argv[2])
partial7_conll_path=os.path.abspath(sys.argv[3])
partial5_conll_path=os.path.abspath(sys.argv[4])
partial1_conll_path=os.path.abspath(sys.argv[5])
model_dir=os.path.abspath(sys.argv[6])+'/'
iter1=str(int(sys.argv[7]))
iter2=str(int(sys.argv[8]))
iter3=str(int(sys.argv[9]))
iter4=str(int(sys.argv[10]))
embed_path = ''
if len(sys.argv)>11:
	embed_path = os.path.abspath(sys.argv[11])

dev_path = ''
if len(sys.argv)>12:
	dev_path = os.path.abspath(sys.argv[12])

mst2conll=curr_dir+'mst2conll.py'
conll2mst=curr_dir+'conll2mst.py'
get_best_tree=curr_dir+'get_best_trees_by_score.py'

print os.getcwd()
##############################################################################################################
#####                                           TRAINING FULL                                            #####
##############################################################################################################
print colored('training on full_conll_path','red')

command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+full_conll_path+' --epochs '+iter1+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path
if embed_path =='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+full_conll_path+' --epochs '+iter1+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl'
if dev_path!='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+full_conll_path+' --epochs '+iter1+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path +' --dev '+dev_path

	
print command
os.system(command)

##############################################################################################################
command = 'cp '+ model_dir+'barchybrid.model'+iter1 + ' '+model_dir+'/full.model'
print command 
os.system(command)

command = 'cp '+model_dir+'/params.pickle '+ model_dir+'/full.params.pickle'
print command
os.system(command)

print colored('partially parsing partial 7 trees','red')
command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial7_conll_path+' --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle --extrn '+embed_path
if embed_path =='':
	command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial7_conll_path+' --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle'

print command
os.system(command)

train_file = model_dir+'train.conll'
os.system('cat '+full_conll_path+' '+model_dir+'test_pred.conll > '+train_file)

##############################################################################################################
#####                                           TRAINING PARTIAL 7                                       #####
##############################################################################################################
print colored('training on partial7_conll_path','red')

command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter2+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path
if embed_path =='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter2+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl'
if dev_path!='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter2+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path +' --dev '+dev_path

print command
os.system(command)

###############################################################################################################

command = 'cp '+ model_dir+'barchybrid.model'+iter2 + ' '+model_dir+'/partial7.model'
print command 
os.system(command)

command = 'cp '+model_dir+'/params.pickle '+ model_dir+'/partial7.params.pickle'
print command
os.system(command)

print colored('partially parsing partial 5 trees','red')
command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial5_conll_path+'  --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle --extrn ' + embed_path
if embed_path =='':
	command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial5_conll_path+'  --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle'

print command
os.system(command)

os.system('cat '+full_conll_path+' '+model_dir+'test_pred.conll > '+train_file)

##############################################################################################################
#####                                           TRAINING PARTIAL 5                                       #####
##############################################################################################################
print colored('training on partial5_conll_path','red')

command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter3+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path
if embed_path =='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter3+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl '
if dev_path!='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter3+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path +' --dev '+dev_path
print command
os.system(command)

###############################################################################################################
command = 'cp '+ model_dir+'barchybrid.model'+iter3 + ' '+model_dir+'/partial5.model'
print command 
os.system(command)

command = 'cp '+model_dir+'/params.pickle '+ model_dir+'/partial7.params.pickle'
print command
os.system(command)

print colored('partially parsing partial 1 trees','red')
command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial1_conll_path+'  --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle --extrn '+embed_path
if embed_path =='':
	command='nice python -u '+parser_path+' --predict --partial --outdir '+model_dir+'/ --test '+partial1_conll_path+'  --model '+model_dir+'barchybrid.model'+iter1+' --params '+model_dir+'/params.pickle '
print command
os.system(command)

os.system('cat '+full_conll_path+' '+model_dir+'test_pred.conll > '+train_file)


##############################################################################################################
#####                                           TRAINING PARTIAL ALL                                     #####
##############################################################################################################
print colored('training on partial_all_conll_path','red')
command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+' --train '+train_file+' --epochs '+iter4+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path
if embed_path =='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+' --train '+train_file+' --epochs '+iter4+' --lstmdims 125 --lstmlayers  2 --bibi-lstm --k 3 --usehead --userl '
if dev_path!='':
	command='nice python -u '+ parser_path+' --cnn-seed 123456789 train --outdir '+model_dir+'/ --train '+train_file+' --epochs '+iter4+' --lstmdims 125 --lstmlayers 2 --bibi-lstm --k 3 --usehead --userl --extrn  ' +embed_path +' --dev '+dev_path

print command
os.system(command)

print colored('finish... AHL!','red')
