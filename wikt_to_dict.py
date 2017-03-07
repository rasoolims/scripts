import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
   print 'wikt_dict src_lang dst_lang output_folder'

src = sys.argv[2]
dest = sys.argv[3]

output_folder = os.path.abspath(sys.argv[4])+'/'
writer1 = codecs.open(output_folder+src+'2'+dest, 'w')
writer2 = codecs.open(output_folder+dest+'2'+src, 'w')

for line in codecs.open(os.path.abspath(sys.argv[1]),'r'):
   spl = line.strip().split('\t')
   if len(spl)<3: continue

   if spl[1]==dest:
      for w in spl[2:]:
         w_p = w.replace('_',' ')
         writer1.write(spl[0] + '\t' + w_p + '\n')
         writer2.write(w_p + '\t' + spl[0] + '\n')

writer1.close()
writer2.close()
