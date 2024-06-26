import os
import re
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

#change the files to the root
files=os.listdir('./fire2017data')
files.sort() 
# Remove 'putusan_pidana(1).txt' from the list if it exists
if 'putusan_pidana_(01).txt' in files:
    files.remove('putusan_pidana_(01).txt')
title=files
address=[('./fire2017data/'+x) for x in files]

corpus_text=[]

lemmer=WordNetLemmatizer()
for x in range(len(address)):
    f=open(address[x],'r')
    text=f.read()
    f.close()
    text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    unigram = nltk.word_tokenize(text)
    lemWords_unigram_verb=[lemmer.lemmatize(word,pos="v") for word in unigram]
    lemWords_unigram_adverb=[lemmer.lemmatize(word,pos="a") for word in lemWords_unigram_verb]
    item_text=' '.join([lemmer.lemmatize(word, pos="n") for word in lemWords_unigram_adverb])
    corpus_text.append(item_text)


corpus = corpus_text
vectorizer = CountVectorizer()
tf_raw = vectorizer.fit_transform(corpus)
features=vectorizer.get_feature_names_out()

N=len(corpus)
norm=[0]*N
tf_raw_arr=tf_raw.toarray()
ct=0;
posting_list = {i: [] for i in vectorizer.vocabulary_} 
#print(listKeys)
for j in posting_list:
    ct=0
    for i in tf_raw_arr:
        if i[vectorizer.vocabulary_[j]]>0:
            posting_list[j].append((ct,i[vectorizer.vocabulary_[j]]))
            norm[ct]=norm[ct]+(1+math.log10(i[vectorizer.vocabulary_[j]]))**2
        ct=ct+1

print(title)

np.save('posting_list2.npy', posting_list) 
np.save('norm2.npy', norm)
np.save('titles2.npy',title)