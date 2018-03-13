import os,sys,codecs

lines = codecs.open(os.path.abspath(sys.argv[1]), 'r').read().strip().split('\n')
gold_orders = codecs.open(os.path.abspath(sys.argv[2]), 'r').read().strip().split('\n')
orders = codecs.open(os.path.abspath(sys.argv[3]), 'r').read().strip().split('\n')

assert len(lines)==len(orders)

writer = codecs.open(os.path.abspath(sys.argv[4]), 'w')

for i in range(len(lines)):
	words = lines[i].strip().split()
	greorder = [int(o) for o in gold_orders[i].strip().split()]
	greordered = [words[o-1] for o in greorder]
	reorder = [int(o) for o in orders[i].strip().split()]
	reordered = [words[o-1] for o in reorder]
	writer.write('<<<<\n')
	writer.write(' '.join(words)+'\n')
	writer.write(' '.join(greordered)+'\n')
	writer.write(' '.join(reordered)+'\n')
writer.close()