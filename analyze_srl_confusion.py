import os,sys


confusions = open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')


same_conf = 0
all_sc = 0
same_conf_tp = 0
all_sc_tp = 0
diff_conf = 0
all_dc = 0
diff_conf_tp = 0
all_dc_tp = 0
for conf in confusions:
	spl = conf.strip().split()
	freq = float(spl[1])
	prop = float(spl[2])
	src,dst = spl[0].split('-')
	if src==dst:
		same_conf += prop*freq
		all_sc+= freq
		same_conf_tp += prop
		all_sc_tp += 1

	else:
		diff_conf += prop*freq
		all_dc+= freq
		diff_conf_tp += prop
		all_dc_tp += 1
	if freq>50:
		print conf

print '----------------'
print same_conf/all_sc
print diff_conf/all_dc
print '----------------'
print same_conf_tp/all_sc_tp
print diff_conf_tp/all_dc_tp