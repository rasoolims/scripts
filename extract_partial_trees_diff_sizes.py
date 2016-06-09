import os,sys,codecs
from collections import defaultdict

tree_extractor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/extract_trees.py'
partial_extractor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/extract_partial_trees.py'
mst2conll = os.path.dirname(os.path.abspath(sys.argv[0]))+'/mst2conll.py'
word_to_lemma = os.path.dirname(os.path.abspath(sys.argv[0]))+'/put_word_to_lemma.py'
shorter = os.path.dirname(os.path.abspath(sys.argv[0]))+'/remove_long_sentences_from_conll.py'
lang_id = os.path.dirname(os.path.abspath(sys.argv[0]))+'/add_lang_id_to_conll.py'

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder_full = os.path.abspath(sys.argv[2])+'/'
output_folder_par7 = os.path.abspath(sys.argv[3])+'/'
output_folder_par5 = os.path.abspath(sys.argv[4])+'/'
output_folder_par1 = os.path.abspath(sys.argv[5])+'/'
f = sys.argv[6]

# full sentences
command  = 'python '+tree_extractor + ' 1212121212 2121212121 '+input_folder+f + ' '+output_folder_full+f+'.tmp' +' true'
print command
os.system(command)

command  = 'python '+mst2conll + ' '+output_folder_full+f+'.tmp'+' > ' + output_folder_full+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+lang_id + ' '+output_folder_full+f+'.conll.tmp'+' ' +f+' ' + output_folder_full+f+'.conll.tmp.tmp'
print command
os.system(command)

command  = 'python '+word_to_lemma + ' '+output_folder_full+f+'.conll.tmp.tmp'+' ' + output_folder_full+f
print command
os.system(command)


command  = 'python '+tree_extractor + ' 7 0.8 '+input_folder+f + ' '+output_folder_par7+f+'.tmp' +' true'
print command
os.system(command)

command  = 'python '+partial_extractor + ' '+output_folder_par7+f+'.tmp'+' ' + output_folder_par7+f+'.mst.tmp'
print command
os.system(command)

command  = 'python '+mst2conll + ' '+output_folder_par7+f+'.mst.tmp'+' > ' + output_folder_par7+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+shorter + ' '+output_folder_par7+f+'.conll.tmp'+' ' +output_folder_par7+f+'.conll.short.tmp'+' 50'
print command
os.system(command)

command  = 'python '+lang_id + ' '+output_folder_par7+f+'.conll.short.tmp'+' ' +f+' ' + output_folder_par7+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+word_to_lemma + ' '+output_folder_par7+f+'.conll.tmp'+' ' + output_folder_par7+f
print command
os.system(command)


command  = 'python '+tree_extractor + ' 5 0.8 '+input_folder+f + ' '+output_folder_par5+f+'.tmp' +' true'
print command
os.system(command)

command  = 'python '+partial_extractor + ' '+output_folder_par5+f+'.tmp'+' ' + output_folder_par5+f+'.mst.tmp'
print command
os.system(command)

command  = 'python '+mst2conll + ' '+output_folder_par5+f+'.mst.tmp'+' > ' + output_folder_par5+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+shorter + ' '+output_folder_par5+f+'.conll.tmp'+' ' +output_folder_par5+f+'.conll.short.tmp'+' 50'
print command
os.system(command)

command  = 'python '+lang_id + ' '+output_folder_par5+f+'.conll.short.tmp'+' ' +f+' ' + output_folder_par5+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+word_to_lemma + ' '+output_folder_par5+f+'.conll.tmp'+' ' + output_folder_par5+f
print command
os.system(command)



command  = 'python '+tree_extractor + ' 1 0.8 '+input_folder+f + ' '+output_folder_par1+f+'.tmp' +' true'
print command
os.system(command)

command  = 'python '+partial_extractor + ' '+output_folder_par1+f+'.tmp'+' ' + output_folder_par1+f+'.mst.tmp'
print command
os.system(command)

command  = 'python '+mst2conll + ' '+output_folder_par1+f+'.mst.tmp'+' > ' + output_folder_par1+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+shorter + ' '+output_folder_par1+f+'.conll.tmp'+' ' +output_folder_par1+f+'.conll.short.tmp'+' 50'
print command
os.system(command)

command  = 'python '+lang_id + ' '+output_folder_par1+f+'.conll.short.tmp'+' ' +f+' ' + output_folder_par1+f+'.conll.tmp'
print command
os.system(command)

command  = 'python '+word_to_lemma + ' '+output_folder_par1+f+'.conll.tmp'+' ' + output_folder_par1+f
print command
os.system(command)








