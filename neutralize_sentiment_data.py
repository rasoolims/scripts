import os,sys,codecs

gold_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(gold_folder):
	print f
	writer = codecs.open(output_folder+f,'w')
	neut_data = [line.split('\t')[0].strip() + '\tneutral' for line in codecs.open(gold_folder+f,'r')]
	writer.write('\n'.join(neut_data))
	writer.close()