import pandas as pd
import csv
import datetime

class FileSplitter(object):
  """docstring for Preprocessing"""
  def __init__(self, page_id):
     self.page_id = page_id
     self.file = '../data/%s_output/%s_FBScraper_Posts.csv' % (self.page_id, self.page_id)
     self.file_new = '../data/%s_output/%s_posts_split/' % (self.page_id, self.page_id)
        
  def split(self):
    print "\nStarting splitting all Posts from csv file into txt files%s" % (datetime.datetime.now())

    with open(self.file, 'rb') as csvfile:
        confessions =  csv.DictReader(csvfile)
        count = 0
        for row in confessions:
          count += 1
          single_status_message = row['status_message'][6:].strip()
          # start = single_status_message[:5]
          with open(self.file_new + "Output_%s.txt" % count, "w") as file:
            file.write(single_status_message)
            file.close()
    print "Done! splitting all Posts %s" % (datetime.datetime.now())

