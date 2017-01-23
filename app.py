from flask import Flask, render_template, request, json
import nltk
from nltk import word_tokenize
from gensim.summarization import summarize, keywords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import numpy as np
import pandas as pd
from lda_summarization import summarize_methods
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize1():
    _text =  request.form['inputText']
    if _text:
        return  json.dumps(summarizeAlgo(_text))
    else:
        return json.dumps({'html':'<span>Enter the text</span>'})

@app.route('/ldasummarize', methods=['POST'])
def summarize2():
    _text = request.form['inputText']
    if _text:
        return json.dumps(summarize_lda(_text))
    else:
        return json.dumps({'html': '<span>Enter the text</span>'})

def summarizeAlgo(_text): 

    tos_text_paras = _text.split("\n")
    copyright = ['collective work',\
    'compilation',\
    'compulsory license',\
    'copyright',\
    'copyright holder/copyright owner',\
    'copyright notice',\
    'derivative work',\
    'exclusive right',\
    'expression',\
    'fair use',\
    'first sale doctrine',\
    'fixation',\
    'idea',\
    'infringement',\
    'intellectual property',\
    'license',\
    'master use license',\
    'mechanical license',\
    'medium',\
    'moral rights',\
    'musical composition',\
    'parody',\
    'patent',\
    'performing rights',\
    'permission',\
    'public domain',\
    'publication/publish',\
    'right of publicity',\
    'royalty',\
    'service mark',\
    'sound recording',\
    'statutory damages',\
    'synchronization license',\
    'tangible form of expression',\
    'term',\
    'title',\
    'trademark',\
    'trade secret',\
    'work for hire']

    privacy = ['access',\
    'account',\
    'activity',\
    'advertising',\
    'confidentiality',\
    'content',\
    'cookie',\
    'legal',\
    'preferences',\
    'privacy',\
    'protect',\
    'religion',\
    'security',\
    'settings']

    termination = ['cease',\
    'terminate',\
    'remove',\
    'inactive',\
    'suspend',\
    'account',\
    'discontinue',\
    'revoke',\
    'retain']

    copyright_all,privacy_all,termination_all = [],[],[]


    for para in tos_text_paras:
        check = 0
        for word in para.split(" "):
            word = word.lower()
            if word in copyright:
                copyright_all.append(para)
                check = 1
            if word in privacy:
                privacy_all.append(para)
                check = 1
            if word in termination:
                termination_all.append(para)
                check = 1
            if check != 0:
                break

    #ERROR!!!
    # copyright_all = [sent for sent in copyright_all if len(word_tokenize(sent)) > 5]
    #
    # privacy_all = [sent for sent in privacy_all if len(word_tokenize(sent)) > 5]
    #
    # termination_all = [sent for sent in termination_all if len(word_tokenize(sent)) > 5]

    categoryDict = {}

    if (len(copyright_all) != 0):
        if (len(copyright_all) != 1):
            copyright_text = ' '.join(copyright_all)
            # categoryDict["CopyrightFull"] = copyright_all
            copyright_all = summarize(copyright_text, split=True, ratio=.2)
        categoryDict["Copyright"] = copyright_all


    if (len(privacy_all) != 0):
        if (len(privacy_all) != 1):
            privacy_text = ' '.join(privacy_all)
            # categoryDict["PrivacyFull"] = privacy_all
            privacy_all = summarize(privacy_text, split=True, ratio=.02)
        categoryDict["Privacy"] = privacy_all


    if (len(termination_all) != 0):
        if (len(termination_all) != 1):
            termination_text = ' '.join(termination_all)
            # categoryDict["TerminationFull"] = termination_all
            termination_all = summarize(termination_text, split=True, ratio=.2)
        categoryDict["Termination"] = termination_all

    return categoryDict

def summarize_lda(_text):
    tokenizer = RegexpTokenizer(r'\w+')
    #ERROR!!
    #en_stop = set(stopwords.words('english'))
    en_stop = []
    p_stemmer = PorterStemmer()
    topic_dic = {'Privacy': ['privacy', 'cookie', 'confidentiality', 'account'],
                 'Copyright': ['copyright', 'infringement', 'dmca', 'intellectual', 'holder', 'agent', 'trademark', 'content'],
                 'Content Sharing/Use': ['share'],
                 'Cancelation/Termination': ['cease', 'terminate', 'suspend', 'cancel'],
                 'Modification/Pricing': ['modification', 'pricing', 'change']}
    dictionary2 = corpora.Dictionary.load('lda_dictionary')
    ldamodel2 = gensim.models.ldamodel.LdaModel.load('lda_model')
    pars = re.split('\r?\n\r?\n?', _text)
    topic_pars = summarize_methods.create_topic_pars(pars, tokenizer, p_stemmer, en_stop, ldamodel2, dictionary2, topic_dic)
    #print(topic_pars)

    category_dict = {}
    for topic_par in topic_pars:
        cat = topic_par[1]
        par = topic_par[0]
        if (cat not in category_dict):
            category_dict[cat] = [par]
            #category_dict[cat] = [summarize(par)]
        else:
            category_dict[cat].append(par)
            #category_dict[cat].append(summarize(par))

    for topic in category_dict:
        if topic == "Privacy":
            ratio = .02
        else:
            ratio = .1
        category_dict[topic] = summarize(' '.join(category_dict[topic]), split=True, ratio=ratio)

    return category_dict
                                    
if __name__ == "__main__":
    app.run()
