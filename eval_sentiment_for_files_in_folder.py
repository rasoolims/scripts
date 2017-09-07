import os,sys,codecs

script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/eval_sentiment.py'
gold_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(output_folder):
	command = 'python -u '+script+ ' ' + gold_folder+f+' '+output_folder+f
	print command
	os.system(command)