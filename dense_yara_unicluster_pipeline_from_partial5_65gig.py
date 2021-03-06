import sys,codecs,os
from termcolor import colored

if len(sys.argv)<12:
	print colored('arguments: yara_jar full_conll_path partial7_conll_path partial5_conll_path partial_all_conll_path model_path iter1 iter2 iter3 iter4 target_dir cluster_path gold_test_file','red')
	sys.exit(0)

print colored('reading arguments','red')
curr_dir=os.path.dirname(os.path.realpath(__file__))+'/'

yara_jar=os.path.abspath(sys.argv[1])
full_conll_path=os.path.abspath(sys.argv[2])
partial7_conll_path=os.path.abspath(sys.argv[3])
partial5_conll_path=os.path.abspath(sys.argv[4])
partial_all_conll_path=os.path.abspath(sys.argv[5])
model_path=os.path.abspath(sys.argv[6])
iter1=str(int(sys.argv[7]))
iter2=str(int(sys.argv[8]))
iter3=str(int(sys.argv[9]))
iter4=str(int(sys.argv[10]))
target_dir=os.path.abspath(sys.argv[11])
cluster_path=os.path.abspath(sys.argv[12])
gold_test_file=os.path.abspath(sys.argv[13])

mst2conll=curr_dir+'mst2conll.py'
conll2mst=curr_dir+'conll2mst.py'
get_best_tree=curr_dir+'get_best_trees_by_score.py'



##############################################################################################################
#####                                           TRAINING PARTIAL 5                                       #####
##############################################################################################################
print colored('training on partial5_conll_path','red')
train_file =partial5_conll_path+'.filled.top200k+full.conll'
command='nice java -jar -Xmx65g '+ yara_jar+' train -cluster_id '+cluster_path+' -train-file '+train_file+' -model '+model_path+'.partial5 iter:'+iter3
os.system(command)

###############################################################################################################

print colored('partially parsing partial all trees','red')
command='nice java -jar -Xmx65g '+yara_jar+' parse_partial -model '+model_path+'.partial5_iter'+iter3+' -input '+partial_all_conll_path +' -output '+partial_all_conll_path+'.filled -score '+partial_all_conll_path+'.score'
os.system(command)

print colored('convert filled trees to mst','red')
os.system('python '+conll2mst+' '+partial_all_conll_path+'.filled > '+partial_all_conll_path+'.filled.mst')

print colored('get best 200k trees for partial all trees','red')
os.system('python '+get_best_tree+' '+partial_all_conll_path+'.filled.mst '+partial_all_conll_path+'.score 200000 '+partial_all_conll_path+'.filled.top200k.mst')

print colored('convert 200k best to conll','red')
os.system('python '+mst2conll+' '+partial_all_conll_path+'.filled.top200k.mst > '+partial_all_conll_path+'.filled.top200k.conll')

print colored('concatenate to the full trees','red')
train_file =partial_all_conll_path+'.filled.top200k+full.conll'
os.system('cat '+full_conll_path+' '+partial_all_conll_path+'.filled.top200k.conll > '+train_file)

##############################################################################################################
#####                                           TRAINING PARTIAL ALL                                     #####
##############################################################################################################
print colored('training on partial_all_conll_path','red')

command='nice java -jar -Xmx65g '+ yara_jar+' train -cluster_id '+cluster_path+' -train-file '+train_file+' -model '+model_path+'.partial_all iter:'+iter4
os.system(command)

print colored('copying model 4 to the target_dir','red')
os.system('cp '+model_path+'.partial_all_iter'+iter4+' '+target_dir+'/')

print colored('getting test results','red')
command='nice java -jar -Xmx65g '+ yara_jar+ ' parse_conll -model '+model_path+'.partial_all_iter'+iter4+' -input '+gold_test_file +' -output '+model_path+'.test'
os.system(command)

print colored('evaluating the test results','red')
command='nice java -jar -Xmx65g '+ yara_jar+ ' eval -gold '+gold_test_file +' -parsed '+model_path+'.test'
os.system(command)

print colored('finish... AHL!','red')


