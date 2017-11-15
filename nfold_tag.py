import sys,codecs,os

lines =codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
fold_num=int(sys.argv[2])
output_path = os.path.abspath(sys.argv[3])

folds = [list() for _ in range(fold_num)]

part_size = len(lines)/fold_num
index = 0
for i in range(fold_num):
	if i<fold_num -1:
		folds[i] = lines[index: index+ part_size]
	else:
		folds[i] = lines[index:]
	index += part_size


for i in range(fold_num):
	test_fold = folds[i]
	train_fold = []
	for j in range(fold_num):
		if i!=j:
			train_fold += folds[j]
	codecs.open(output_path+'.train.'+str(i+1), 'w').write('\n'.join(train_fold)+'\n')
	codecs.open(output_path+'.dev.'+str(i+1), 'w').write('\n'.join(test_fold)+'\n')
