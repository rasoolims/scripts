import sys,os,codecs
from termcolor import colored

if len(sys.argv)<11:
	print 'run_yara_ss_pipeline_with_cut_off.py [jar_path] [full_iter#] [model_path] [full_tree_path] [partial_tree_path] [dev_path] [gold_dev_path] [punc_path] [last_iter#] [cut_off]'
	sys.exit(0)
	
curr_dir=os.path.abspath(sys.argv[0])[:os.path.abspath(sys.argv[0]).rfind('/')]+'/'
jar_path=os.path.abspath(sys.argv[1])
full_iter=int(sys.argv[2])
model_path=os.path.abspath(sys.argv[3])

full_tree_path=os.path.abspath(sys.argv[4])
partial_tree_path=os.path.abspath(sys.argv[5])
dev_path=os.path.abspath(sys.argv[6])
gold_dev_path=os.path.abspath(sys.argv[7])
punc_path=os.path.abspath(sys.argv[8])
last_iter=int(sys.argv[9])
cut_off=int(sys.argv[10])

beam=64
nt=16

'''
	step 1: train on full trees
'''
print colored('step 1: train on full trees','red')
m_file=model_path+"_step1"
# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ full_tree_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(1))
# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --inf-file '+m_file +' --model-file '+m_file+'_iter'+str(1) )
# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


'''
	step 2: parse the full trees
'''
print colored('step 2: parse the full trees','red')
full_parsed1_path=m_file+'.full.parse1.conll'
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+full_tree_path+' --out '+full_parsed1_path+' --inf-file '+m_file +' --model-file '+m_file+'_iter'+str(1))

'''
	step 3: train on new full tress
'''
print colored('step 3: train on new full tress','red')
m_file=model_path+"_step3"

# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ full_parsed1_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(1))

# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --inf-file '+m_file +' --model-file '+m_file+'_iter'+str(1) )

# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)

'''
	step 4: parse full trees and parse_partial partial tress (concat them)
'''
print colored('step 4: parse full trees and parse_partial partial tress (concat them)','red')
full_parsed2_path=m_file+'.full.parse2.conll'
partial_parsed2_path=m_file+'.partial.parse2.conll'
all_parsed2_path=m_file+'.all.parse2.conll'

# parse the train data again
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+full_tree_path+' --out '+full_parsed2_path+' --inf-file '+m_file +' --model-file '+ m_file+'_iter'+str(1))

# constraint parse the partial data
os.system('nice java -Xmx20g -jar '+jar_path+' parse_partial --test-file '+partial_tree_path+' --out '+partial_parsed2_path+' --inf-file '+m_file +' --model-file '+ m_file+'_iter'+str(1))

# concatenate the files
os.system('cat '+full_parsed2_path+' '+partial_parsed2_path+' >'+all_parsed2_path)


'''
	step 5: train on the concatenated file
'''
print colored('step 5: train on the concatenated file','red')
m_file=model_path+"_step5"

# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ all_parsed2_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(full_iter))

# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --inf-file '+m_file +' --model-file '+m_file+'_iter'+str(full_iter) )

# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


'''
	step 6: reparse the concatenated file
'''
print colored('step 6: reparse the concatenated file','red')
all_parsed3_path=m_file+'.all.parse3.conll'
score_file=m_file+'.scores'

# parse the train data again
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+all_parsed2_path+' --out '+all_parsed3_path+' --inf-file '+m_file +' --model-file '+ m_file+'_iter'+str(full_iter) +' --score-file '+score_file)

# convert to mst format
os.system('python '+curr_dir+'conll2mst.py '+all_parsed3_path+' > '+all_parsed3_path+'.mst')

# get best scoring trees
os.system('python '+curr_dir+'get_best_trees_by_score.py '+all_parsed3_path+'.mst '+score_file+' '+str(cut_off)+' '+all_parsed3_path+'.mst.pruned')

# convert to conll format
os.system('python '+curr_dir+'mst2conll.py '+all_parsed3_path+'.mst.pruned'+' > '+all_parsed3_path+'.pruned')

all_parsed4_path=all_parsed3_path+'.pruned'

'''
	step 7: re-train on the concatenated file
'''
print colored('step 7: re-train on the parsed concatenated file','red')
m_file=model_path+"_step7"

# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ all_parsed4_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(last_iter))

# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --inf-file '+m_file +' --model-file '+m_file+'_iter'+str(last_iter) )

# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


print colored('DONE!','red')