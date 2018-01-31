import sys,os,codecs, random
from collections import defaultdict
import threading
 
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

def create_noise(target_lang, target_path, dict_path, k, output_path):
    target_sentences = codecs.open(target_path,'r').read().strip().split('\n') 
    target_words = dict()
    bin_info = defaultdict(list)
    for line in codecs.open(dict_path,'r'):
        f = line.strip().split()
        if len(f)==3:
            word, prob, bin = f[0], float(f[1]), int(f[2])
            bin_info[bin].append(f[0])
            target_words[word] = (prob, bin)

    output_writer = codecs.open(output_path,'w')


    for i in range(len(target_sentences)):
        output = list()
        output.append(target_lang)

        output.append(target_sentences[i])
        words, tags = [], []
        
        for spl in target_sentences[i].strip().split():
            tind = spl.rfind('_')
            words.append(spl[:tind])
            tags.append(spl[tind+1:])

        rw = random.randint(0, len(words)-1)
        prob = target_words[words[rw]][0] if words[rw] in target_words else 1e-10
        output.append(str(prob))

        for j in range(len(words)):
            sample = [w for w in words]
            bin_number = target_words[sample[j]][1] if sample[j] in target_words else 0

            if bin_number>0:
                tw = bin_info[bin_number]
                for k_ in range(k):
                    r = random.randint(0, len(tw)-1)
                    sample[j] = tw[r]
                    prob = target_words[sample[j]][0]

                    new_output = ' '.join([sample[f]+'_'+tags[f] for f in range(len(words))]) + '\t'+ str(prob)
                    output.append(new_output)

        output_writer.write('\t'.join(output)+'\n')
        if (i+1)%100==0:
            sys.stdout.write(str(i+1)+'...')

    output_writer.close()
    sys.stdout.write('\n')
    os.system('ls -lah '+output_path)
    os.system('gzip '+output_path)
    os.system('ls -lah '+output_path+'.gz')

bible_folder = os.path.abspath(sys.argv[1])+'/'
dict_path = os.path.abspath(sys.argv[2])+'/'
k = int(sys.argv[3])
output_folder =  os.path.abspath(sys.argv[4]) +'/'

threads = []
for lang in os.listdir(bible_folder):

    print lang
    t = FuncThread(create_noise, lang, bible_folder+lang, dict_path+lang, k, output_folder+lang)
    threads.append(t)

    #create_noise(l2, l1, l2_tag, l1_tag, l1_dict, k, o2_path)
    if len(threads)>=16:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        threads = []

if len(threads)>0:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        threads = []