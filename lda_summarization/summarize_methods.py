from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import numpy as np
import pandas as pd

def read_file_to_paragraphs(file_path):
    file = open(file_path, 'r')
    doc = file.read()
    file.close()
    pars = re.split('\n\n+', doc)
    #print('reading %s wich have %d paragraphs' % (file_path, len(pars)))
    return(pars)

def tokenize_and_stem(text, tokenizer, stemmer, stop_words):
    return([stemmer.stem(word) for word in tokenizer.tokenize(text.lower()) if word not in stop_words])

def create_topic_pars(pars, tokenizer, stemmer, stop_words, ldamodel, word_dictionary, topic_dictionary):
    norm_pars = [tokenize_and_stem(par, tokenizer, stemmer, stop_words) for par in pars]
    #print('created normalized paragraphs object of length %d' % len(norm_pars))
    bows = [word_dictionary.doc2bow(text) for text in norm_pars]
    #print('created bag-of-words object of length %d' % len(bows))
    topic_pars = []
    for idx, val in enumerate(bows):
        lda_vector = ldamodel[val]
        topic_pars.append([ldamodel.print_topic(max(lda_vector, key=lambda item: item[1])[0]), pars[idx]])

    #print(topic_pars)
    tagged_pars = []
    for topic_name in topic_dictionary:
        topic_words = topic_dictionary[topic_name]
        for pars in topic_pars:
            topic = pars[0]
            par = pars[1]
            if (len(par) > 50):
                for word in topic_words:
                    if stemmer.stem(word) in topic:
                        tagged_pars.append([par, topic_name])
                        break
    return (tagged_pars)