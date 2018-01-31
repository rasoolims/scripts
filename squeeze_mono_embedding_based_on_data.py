import os,sys,gzip,codecs
from collections import defaultdict
reload(sys)
sys.setdefaultencoding('utf8')

lang_dict = defaultdict(set)
for li, line in enumerate(gzip.open(os.path.abspath(sys.argv[1]), 'r')):
    spl = line.strip().split('\t')
    for i in range(0, len(spl), 2):
        lang_id = spl[i].strip()
        for sen_t in spl[i+1].strip().split():
            r = sen_t.rfind('_')
            lang_dict[lang_id].add(sen_t[:r])
    if (li+1)%1000 ==0:
        sys.stdout.write(str(li+1)+'...')
print ''

input_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'
for lang in lang_dict.keys():
    sys.stdout.write(str(lang)+'...')
    lang_dict[lang].add('_UNK_')
    lang_dict[lang].add('NUM')
    writer = gzip.open(output_folder+lang+'.gz', 'w')
    for line in gzip.open(input_folder+lang+'.gz', 'r'):
        if line.strip().split()[0] in lang_dict[lang]:
            writer.write(line.strip()+'\n')
    writer.close()

print 'done!'