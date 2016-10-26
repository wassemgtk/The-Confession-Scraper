# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
import numpy
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import csv
import glob
import pprint

# class TopicModel(object):
#   """docstring for TopicModel"""
#   def __init__(self):
#     self.arg = 0
    
def tf(word, blob):
  return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
  return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
  return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
  return tf(word, blob) * idf(word, bloblist)

# def train(self):
bloblist = list()

with open('../../output/BigRedConfessions_facebookScraper_Posts.csv', 'rb') as csvfile:
  confessions =  csv.DictReader(csvfile)
  for row in confessions:
      content = row['status_message'][5:].strip()
      stop = set(stopwords.words('english'))
      content_new = [i for i in content.lower().split() if i not in stop]
      str1 = ' '.join(e.decode("ascii", "ignore") for e in content_new)
      doc = tb(str1)
      bloblist.append(doc)
# # print bloblist
all_bloblists = []
for i, blob in enumerate(bloblist):
    words_bloblist = []
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:20]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
        words_bloblist.append(word)
    all_bloblists.append(words_bloblist)
print all_bloblists

dictionary = corpora.Dictionary(all_bloblists)
dictionary.save('output_topic_modeling/test.dict')
corpus = [dictionary.doc2bow(text) for text in all_bloblists]
corpora.MmCorpus.serialize('output_topic_modeling/test_2.mm', corpus)

# This is LDA implementation change parameters accordingly
id2word = dictionary
mm = corpus
lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=25, update_every=1, chunksize=50, passes=10)

# Saving topic model list to file and printing on screen
open('output_topic_modeling/ldamodel.model', 'w')
lda.save('output_topic_modeling/ldamodel.model')
f = open('output_topic_modeling/ldamodel.txt', 'w')
f.write(str(lda.print_topics(25)))
f.close()
pprint.pprint(lda.print_topics(25))