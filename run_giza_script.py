import os

giza_bin_dir=sys.argv[1]
src_vcb_file=sys.argv[2]
dst_vcb_file=sys.argv[3]
cooc_file=sys.argv[4]
dir_path=sys.argv[5]
src_lang_type=sys.argv[6]
trgt_lang_type=sys.argv[7]


os.system(giza_bin_dir+'GIZA++ -S  '+src_vcb_file+ ' -T '+dst_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file+' -o '+dir_path+src_lang_type+'_'+trgt_lang_type+'.align '+' > '+dir_path+'s_t_nohup.out')

print '(MSR_MESSAGE) done giza'+src_lang_type+'->'+trgt_lang_type+'!'
