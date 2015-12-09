import sys,codecs,os
from numpy import array
from numpy import dot
from numpy import linalg
from collections import defaultdict

def read_normalized_embeddings(embedding_path):
    """Read embeddings from the given path."""
    embedding = {}
    dim = 0
    with open(embedding_path, "r") as embedding_file:
        for line in embedding_file:
            tokens = line.split()
            if len(tokens) > 0:
                word = tokens[1]
                values = []
                for i in range(2, len(tokens)):
                    values.append(float(tokens[i]))
                if dim:
                    assert len(values) == dim
                else:
                    dim = len(values)
                embedding[word] = array(values)
                embedding[word] /= linalg.norm(embedding[word])
    return embedding, dim

def show_similar(embedding, dim, lang_words, src_lang, target_lang):
    best_src_words = defaultdict(dict)
    best_trg_words = defaultdict(dict)


    rare_count1 = 0
    rare_count2 = 0
    print 'size of lang_words '+str(len(lang_words[src_lang]))+','+str(len(lang_words[target_lang]))
    count = 0
    for word1 in lang_words[src_lang]:
        neighbors = []
        best_trg_words[word1] = dict()
        best_src_words[word1] = dict()

        for word2 in lang_words[src_lang]:
            if word1 == word2:
                continue
            else:
                continue
            if word1 in embedding and word2 in embedding:
                cosine = dot(embedding[word1], embedding[word2])
                neighbors.append((cosine, word2))
            else:
                rare_count1 += 1

        neighbors.sort(reverse=True)
        for i in range(min(30, len(neighbors))):
            cosine, buddy = neighbors[i]
            best_src_words[word1][buddy] = cosine

        neighbors = []
        for word2 in lang_words[target_lang]:
            if word1 in embedding and word2 in embedding:
                cosine = dot(embedding[word1], embedding[word2])
                neighbors.append((cosine, word2))
            else:
                rare_count2+=1

        neighbors.sort(reverse=True)
        for i in range(min(30, len(neighbors))):
            cosine, buddy = neighbors[i]
            if cosine>0.7:
                best_trg_words[word1][buddy] = cosine

        count+=1
        if count%4000==0:
            break
            sys.stdout.write(str(count)+'...')

    sys.stdout.write(str(count)+'\n')
    print 'rare count',rare_count1,rare_count2
    return best_src_words, best_trg_words


    

def read_lang_words(dict_path):
    lang_words = defaultdict(set)
    reader = codecs.open(dict_path,'r')
    line = reader.readline()
    while line:
        spl = line.strip().split('\t')
        if len(spl)==2:
            lang_words[spl[0]].add(spl[1])
        line = reader.readline()
    print lang_words.keys()
    return lang_words


if __name__ == "__main__":
    # Path to word embeddings file.
    EMBEDDING_PATH = sys.argv[1]
    embedding, dim = read_normalized_embeddings(EMBEDDING_PATH)
    lang_words = read_lang_words(os.path.abspath(sys.argv[2]))

    best_src_words, best_trg_words = show_similar(embedding, dim, lang_words, sys.argv[3], sys.argv[4])
    writer = codecs.open(os.path.abspath(sys.argv[5]),'w')

    for src_word in best_src_words.keys():
        #for s1 in best_src_words[src_word].keys():
            #writer.write('s\t'+src_word+'\t'+s1+'\t'+str(best_src_words[src_word][s1])+'\n')
        for s2 in best_trg_words[src_word].keys():
            writer.write('t\t'+src_word+'\t'+s2+'\t'+str(best_trg_words[src_word][s2])+'\n')

    writer.close()
