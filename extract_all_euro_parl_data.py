import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<2:
	print 'python extract_all_euro_parl_data.py [aligner_script_path] [euro_parl_dir_path]'
	sys.exit(0)

aligner_script_path=os.path.abspath(sys.argv[1])
dir_path=os.path.abspath(sys.argv[2])+'/'

os.chdir(dir_path)

dirs=os.listdir(dir_path)
for i in range(0,len(dirs)):
	for j in range(i+1,len(dirs)):
		if not dirs[i].endswith('en') or not dirs[j].endswith('en'):
			continue
		new_name=dirs[i][0:dirs[i].find('_')]+'_'+dirs[j][0:dirs[j].find('_')]+'/'
		print new_name
		sys.stdout.flush()
		if not os.path.exists(new_name):
			os.makedirs(new_name)

		f1= os.listdir(dirs[i])
		src1=dir_path+'/'+dirs[i]+'/'+f1[0]
		dst1=dir_path+'/'+dirs[i]+'/'+f1[1]
		if not src1.endswith('en'):
			src1=dir_path+'/'+dirs[i]+'/'+f1[1]
			dst1=dir_path+'/'+dirs[i]+'/'+f1[0]

		s1=dst1[dst1.rfind('.')+1:]

		f2= os.listdir(dirs[j])
		src2=dir_path+'/'+dirs[j]+'/'+f2[0]
		dst2=dir_path+'/'+dirs[j]+'/'+f2[1]
		if not src2.endswith('en'):
			src2=dir_path+'/'+dirs[j]+'/'+f2[1]
			dst2=dir_path+'/'+dirs[j]+'/'+f2[0]

		s2=dst2[dst2.rfind('.')+1:]

		srcw=dir_path+'/'+new_name+'en_'+s1+'_'+s2+'.en'
		dst1_w=dir_path+'/'+new_name+'en_'+s1+'_'+s2+'.'+s1
		dst2_w=dir_path+'/'+new_name+'en_'+s1+'_'+s2+'.'+s2

		sys.stdout.flush()
		os.system('python '+aligner_script_path+' '+src1+' '+dst1+' '+src2+' '+dst2+' '+srcw+' '+dst1_w+' '+dst2_w)
