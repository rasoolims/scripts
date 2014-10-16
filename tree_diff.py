import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<3:
	print 'python tree_diff.py [src_mst_file] [dst_mst_file] [matched_trees]'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
matched_mst_writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

# reading source tree files
sys.stdout.write('reading source tree files...')
sys.stdout.flush()

all_deps=0
all_retrived_deps=0
correct_deps=0

line=src_mst_reader.readline()
dst_line=dst_mst_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=src_mst_reader.readline().strip().split('\t')
		labels=src_mst_reader.readline().strip().split('\t')
		hds=src_mst_reader.readline().strip().split('\t')
		heads=list()

		is_full=True
		for h in hds:
			if h=='-1':
				is_full=False
			heads.append(int(round(float(h))))

		dst_words=dst_line.strip().split('\t')
		dst_tags=dst_mst_reader.readline().strip().split('\t')
		dst_labels=dst_mst_reader.readline().strip().split('\t')
		dst_hds=dst_mst_reader.readline().strip().split('\t')
		dst_heads=list()
		final_heads=list()
		final_labs=list()
		for h in dst_hds:
			dst_heads.append(int(round(float(h))))	
			final_heads.append('-1')	
			final_labs.append('_')

		for i in range(0,len(dst_heads)):
			all_deps+=1
			if dst_heads[i]!=-1:
				all_retrived_deps+=1
				if dst_heads[i]==heads[i]:
					correct_deps+=1
					final_heads[i]=str(heads[i])


		matched_mst_writer.write('\t'.join(words)+'\n')
		matched_mst_writer.write('\t'.join(tags)+'\n')
		matched_mst_writer.write('\t'.join(final_labs)+'\n')
		matched_mst_writer.write('\t'.join(final_heads)+'\n\n')

		if line_count%10000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=src_mst_reader.readline()
	dst_line=dst_mst_reader.readline()

matched_mst_writer.flush()
matched_mst_writer.close()

print ''
print correct_deps,all_retrived_deps,all_deps
precision=float(correct_deps)/all_retrived_deps
recall=float(correct_deps)/all_deps
print 'precision:',precision
print 'recall:',recall