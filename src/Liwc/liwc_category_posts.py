import csv
import pandas as pd
import imp
from os import sys # Unused sys imported from os
LIWC_Index = imp.load_source('LIWC_Index', './Liwc/liwc_helper.py')
from LIWC_Index import LIWC_Index
from os import sys # Reimport 'sys' (imported line 4)
from pandas import DataFrame # Unused DataFrame imported from pandas
import datetime
import string


class LIWC_Posts(object):
    """docstring for Confession"""
    def __init__(self, page_id):
        self.data = []
        self.page_id = page_id
        self.file = '../data/%s_output/%s_FBScraper_Posts.csv' % (self.page_id, self.page_id)
        self.file_new = '../data/%s_output/%s_PostsSentiment.csv' % (self.page_id, self.page_id)
        
    def getLiwcData(self):
        time = datetime.datetime.now()
        print "\nSTARTING with LIWC categorization for positive and negative Posts: %s\n" % (time)
        with open(self.file_new, 'a') as csvfile:
            fieldnames = ['Posemo', 'Negemo', 'Work']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            num_processed = 0

            with open(self.file, 'rb') as csvfile:
              confessions =  csv.DictReader(csvfile)
              all_status_messages = [] # Unused variable 'all_status_messages'
              new = LIWC_Index()
              for row in confessions: 
                single_status_message = row['status_message'][4:].strip()
                count = new.category_matches(single_status_message, ['Posemo', 'Negemo', 'Work'])
                writer.writerow(count)
                num_processed += 1
                if num_processed % 100 == 0:
                  print "%s Posts Processed: %s" % (num_processed, datetime.datetime.now())
            print 'Successfully parsed LIWC dictionary for categorizing positive and negative Posts in: ' + str(datetime.datetime.now() - time)
     
    def addDates(self):
        print '\nStaring to add Dates to categories'
        dates = []
        status_id = []
        len_messages = []
        with open(self.file, 'rb') as csvfile:
            confessions =  csv.DictReader(csvfile)
            all_status_messages = []
            # print confessions
            for row in confessions:
                date = row['status_published']
                s_id = row['status_id']
                mes = row['status_message']
                words = mes.lower().split(' ')
                words_no_punct = [''.join(ch for ch in token if not ch in string.punctuation) for token in words] 
                length = len(words_no_punct)
                dates.append(date)
                status_id.append(s_id)
                len_messages.append(length)

        csv_file = self.file_new
        file = pd.read_csv(csv_file) # Redefining built-in 'file'
        # print len_messages
        file["Date"] = dates
        file["Status_id"] = status_id
        file["length_messages"] = len_messages
        file.to_csv(csv_file, ",")
        final_time = datetime.datetime.now()
        print "DONE with LIWC categorization for positive negative Posts: %s\n" % (final_time)
        
