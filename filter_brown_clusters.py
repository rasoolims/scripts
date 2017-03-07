import os,sys,codecs,operator

lines = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')

words = set()
for l in lines:
	for i in l.strip().split(' '):
		words.add(i) 

cluster_reader =  codecs.open(os.path.abspath(sys.argv[2]),'r')
cluster_writer =  codecs.open(os.path.abspath(sys.argv[3]),'w')

line = cluster_reader.readline()
c = 0
f = 0
while line:
	w = line.strip().split()[1]
	if w in words or w.locut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/ru > /tmp/train_untok_clean/ru
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/bg > /tmp/train_untok_clean/bg
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/en > /tmp/train_untok_clean/en
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/de > /tmp/train_untok_clean/de
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/es > /tmp/train_untok_clean/es
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/pl > /tmp/train_untok_clean/pl
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/hr > /tmp/train_untok_clean/hr
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/hu > /tmp/train_untok_clean/hu
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/pt > /tmp/train_untok_clean/pt
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/sl > /tmp/train_untok_clean/sl
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/sk > /tmp/train_untok_clean/sk
rasooli@mlnlp03 /proj/mlnlp/rasooli $ cut -f1 /proj/mlnlp/rasooli/experiments/sentiment/xlingual/labeled_data/train_untok_clean/sv > /tmp/train_untok_clean/svwer() in words:
		cluster_writer.write(line.strip()+'\n')
	else: f+=1
	c+= 1
	if c%100000 ==0:
		sys.stdout.write(str(c)+'/'+str(f)+'...')
	line = cluster_reader.readline()

cluster_writer.flush()
cluster_writer.close()
print 'done!'