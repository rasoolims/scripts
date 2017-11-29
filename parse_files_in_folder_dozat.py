import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
    print 'input_folder python_path model_path embed_path output_folder'
    sys.exit(0)
input_folder = os.path.abspath(sys.argv[1])+'/'
python_path = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
embed_path = os.path.abspath(sys.argv[4])+'/'
output_folder = os.path.abspath(sys.argv[5])+'/'


print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
    print f
    command = 'nice python -u ' + python_path+ ' --predict --test '+ input_folder+f +' --model '+model_path+f + '/model --params '+ model_path+f+'/params.pickle --output ' + output_folder+f + ' --extrn '+embed_path + f+ '.gz '
    print command
    os.system(command)
