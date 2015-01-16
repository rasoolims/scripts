import sys,os,codecs
from termcolor import colored

if len(sys.argv)<10:
	print 'run_yara_ss_pipeline.py [jar_path] [full_iter#] [model_path] [full_tree_path] [partial_tree_path] [dev_path] [gold_dev_path] [punc_path] [last_iter#]'
	sys.exit(0)
	
jar_path=os.path.abspath(sys.argv[1])
full_iter=int(sys.argv[2])
model_path=os.path.abspath(sys.argv[3])

full_tree_path=os.path.abspath(sys.argv[4])
partial_tree_path=os.path.abspath(sys.argv[5])
dev_path=os.path.abspath(sys.argv[6])
gold_dev_path=os.path.abspath(sys.argv[7])
punc_path=os.path.abspath(sys.argv[8])
last_iter=int(sys.argv[9])

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
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --model-file '+m_file+'_iter'+str(1) )
# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


'''
	step 2: parse the full trees
'''
print colored('step 2: parse the full trees','red')
full_parsed1_path=m_file+'.full.parse1.conll'
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+full_tree_path+' --out '+full_parsed1_path+'  --model-file '+m_file+'_iter'+str(1))

'''
	step 3: train on new full tress
'''
print colored('step 3: train on new full tress','red')
m_file=model_path+"_step3"

# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ full_parsed1_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(full_iter))

# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out  --model-file '+m_file+'_iter'+str(full_iter) )

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
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+full_tree_path+' --out '+full_parsed2_path+'  --model-file '+ m_file+'_iter'+str(full_iter))

# constraint parse the partial data
os.system('nice java -Xmx20g -jar '+jar_path+' parse_partial --test-file '+partial_tree_path+' --out '+partial_parsed2_path+'  --model-file '+ m_file+'_iter'+str(full_iter))

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
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out --model-file '+m_file+'_iter'+str(full_iter) )

# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


'''
	step 6: reparse the concatenated file
'''
print colored('step 6: reparse the concatenated file','red')
all_parsed3_path=m_file+'.all.parse3.conll'

# parse the train data again
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+all_parsed2_path+' --out '+all_parsed3_path+'  --model-file '+ m_file+'_iter'+str(full_iter))

'''
	step 7: re-train on the concatenated file
'''
print colored('step 7: re-train on the parsedconcatenated file','red')
m_file=model_path+"_step7"

# training
os.system('nice java -Xmx20g -jar '+jar_path+' train --train-file '+ all_parsed3_path+' --dev-file '+dev_path+' --model-file '+m_file+' --punc_file '+punc_path+' beam:'+str(beam)+' nt:'+str(nt)+' iter:'+str(last_iter))

# parsing dev
os.system('nice java -Xmx20g -jar '+jar_path+' parse_conll --test-file '+dev_path+' --out '+m_file+'.out  --model-file '+m_file+'_iter'+str(last_iter) )

# evaluating on gold dev
os.system('nice java -Xmx20g -jar '+jar_path+' eval --parsed-file '+m_file+'.out --gold-file '+gold_dev_path +' --punc_file '+punc_path)


print colored('DONE!','red')