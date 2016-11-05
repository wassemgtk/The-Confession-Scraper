#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as array # Unused numpy imported as array
import csv
import string
import datetime
import os, sys # Unused import sys 
import collections # Unused import collections
import itertools
import random
from time import sleep # Unused imports are dead code, bringing no value to the code.
import math


class Emotions(object):
  """docstring for ClassName"""
  def __init__(self, page_id):
    # newpath = r'C:\Program Files\arbitrary' 
    # if not os.path.exists(newpath):
    #     os.makedirs(newpath)
    self.data = []
    self.page_id = page_id
    self.file = '../data/%s_output/%s_FBScraper_Posts.csv' % (self.page_id, self.page_id) 
    self.preprocessed_file = '../data/%s_output/%s_preprocessedEmotions_posts.csv' % (self.page_id, self.page_id) 
    self.file_new = '../data/%s_output/%s_Emotions_posts.csv' % (self.page_id, self.page_id) 
  
  def preprocess(self):
    time = datetime.datetime.now()
    df2 = pd.read_csv(self.file)
    status_new = df2['status_id'][0] # Unused variable 'status_new'
    
    Date = []
    Message = []
    num_array = []
    for i in range(900):
      a = random.sample(range(10, 60), 30)
      a.sort()
      num_array.append(a)
    num_array = list(itertools.chain.from_iterable(num_array))
    num =  0
    k = 0
    for i in range(len(df2['status_published'])):
      b = df2['status_published'][i].split(':')
      k += 1
      try: #Trailing whitespace :p
        num = a[k]
      except IndexError:
        k = 0
        num = a[k]
      bingo = str(num) 
      b.append(bingo)
      b.pop(1)
      new_date = ":".join(b)
      Date.append(new_date)

    for status_message in df2.status_message:
      try:
          val = float(status_message)
          if math.isnan(val) or math.isinf(val): 
            Message.append(' ')
      except ValueError:
        mes = status_message[1:].strip()
        Message.append(mes)

    df2['date'] = Date
    df2['message'] = Message

    df2 = df2.drop('status_message', 1)
    df2 = df2.drop('status_published', 1)
    df2 = df2.drop('status_id', 1)
    df2 = df2.drop('link_name', 1)
    df2 = df2.drop('status_type', 1)
    df2 = df2.drop('num_likes', 1)
    df2 = df2.drop('num_comments', 1)
    df2 = df2.drop('num_shares', 1)
    df2 = df2.drop('status_link', 1)

    df2.to_csv(self.preprocessed_file, sep=',')
    print "Emotions Pre-Processed in: %s" % (datetime.datetime.now()-time)

  
  def train(self):
    print "This will take some time, please have patience: %s" % (datetime.datetime.now())
    num_processed = 0
    time1 = datetime.datetime.now() # Unused variable 'time1'
    with open(self.preprocessed_file,'rb') as csvfile:
      all_dates = []
      all_emotions = []
      all_values = []
      df = pd.read_csv(os.path.join(os.path.dirname(__file__), "emotion_Lexicon.csv"))
      emotion_reader = csv.DictReader(csvfile)
      len_messages = []
      dates = []
      num_processed = 0
      for row in emotion_reader:
        num_processed += 1
        date = row['date']
        single_status_message = row['message']
        words = single_status_message.lower().split(' ')
        words_no_punct = [''.join(ch for ch in token if not ch in string.punctuation) for token in words] 
        
        length = len(words_no_punct)
        len_messages.append(length)
        dates.append(date)

        emotion_index = []
        emotions_in_message = []
        emotions_count = []

        for word in words_no_punct:
          if any(df['TargetWord'] == word):
            df2 =  pd.DataFrame(df.loc[df['TargetWord'] == word, 'AssociationFlag'] == 1)
            
            try:
              a = df2[df2['AssociationFlag'] == True].index.values
              emotion_index.append(a)
            except KeyError:
              pass

        for i in emotion_index:
          if i.size is not 0:
            for k in i:
              emotions = df.get_value(k, 'AffectCategory')
              emotions_in_message.append(emotions)
              to_set = emotions_in_message

        emotion_set = ['positive', 'joy','anticipation', 'trust', 'surprise', 'anger',  'disgust',  'fear', 'sadness', 'negative']

        date, length # Statements that don't have any side-effect and whose return value isn't used.
        for entry in emotion_set:
          count = emotions_in_message.count(entry)
          value =  float(count)/float(length)
          all_dates.append(date)
          all_values.append(value)
          all_emotions.append(entry)
          # w.writerow([date, key, value])
    columns = ['date', 'key', 'value']
    df5 = pd.DataFrame(columns=columns)
    df5['date'] = all_dates
    df5['key'] = all_emotions
    df5['value'] = all_values
    df5.to_csv(self.file_new, sep=',')
    # df5 = df5.append(df5)
    
