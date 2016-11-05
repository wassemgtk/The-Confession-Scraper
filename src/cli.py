import click
from functools import partial # Unused partial imported from functools
import os
import sys # Unused import sys
import imp
# importing files

PostScraper = imp.load_source('PostScraper', './Scraper/scraper_posts.py')
from PostScraper import PostScraper
# CommentScraper = imp.load_source('CommentScraper', './Scraper/scraper_comments.py')
LIWC_Words = imp.load_source('LIWC_Posts', './Liwc/liwc_category_posts.py')
from LIWC_Posts import LIWC_Posts
RevealWordsOfPosts = imp.load_source('RevealWordsOfPosts', './Liwc/liwc_reveal_words_posts.py')
from RevealWordsOfPosts import RevealWordsOfPosts
# LIWC_Comments = imp.load_source('LIWC_Comments', './Liwc/liwc_comments.py')

Emotions = imp.load_source('Emotions', './Emotions/get_emotions.py')
from Emotions import Emotions

FileSplitter = imp.load_source('FileSplitter', './TopicModel/preprocessing_files.py')
from FileSplitter import FileSplitter
runR = imp.load_source('runR', './TopicModel/run_lda.py')
from runR import runR

def get_access_token_page_id(URL):
  page_id = URL.split("/")[-2]
  app_id = ""
  app_secret = "" # DO NOT SHARE WITH ANYONE!
  access_token = app_id + "|" + app_secret
  return page_id, access_token

def create_directories(page_id):
  filename = '../data/%s_output/%s_FBScraper_Posts.csv' % (page_id, page_id)
  if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError: # Guard against race condition
        print 'Error'

def create_directory_for_topic_model(page_id):
  filename = '../data/%s_output/%s_posts_split/Output_1.txt' % (page_id, page_id)
  if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError: # Guard against race condition
        print 'Error'


@click.group()
def cli():
    pass

@cli.command()
@click.argument('greeting', default='Hello')
@click.option('--name', '-n', default='World')
def hello(greeting, name):
    print "{} {}!".format(greeting, name)

@cli.command()
@click.option('--url', '-u', default='https://www.facebook.com/BigRedConfessions/')
def scrape(url):
  page_id_and_access_token = get_access_token_page_id(url)
  page_id = page_id_and_access_token[0]
  access_token = page_id_and_access_token[1]
  create_directories(page_id)
  PostScraper(page_id, access_token).scrapeFacebookPageFeedStatus()

@cli.command()
@click.option('--url', '-u', default='https://www.facebook.com/BigRedConfessions/')
def liwc(url):
  page_id_and_access_token = get_access_token_page_id(url)
  page_id = page_id_and_access_token[0]
  LIWC_Posts(page_id).getLiwcData()
  LIWC_Posts(page_id).addDates()
  Revealer  = RevealWordsOfPosts(page_id).getLiwcWords() # Unused variable 'Revealer'

@cli.command()
@click.option('--url', '-u', default='https://www.facebook.com/BigRedConfessions/')
def emotion(url):
  page_id_and_access_token = get_access_token_page_id(url)
  page_id = page_id_and_access_token[0]
  Emotionizer = Emotions(page_id)
  Emotionizer.preprocess()
  Emotionizer.train()

@cli.command()
@click.option('--url', '-u', default='https://www.facebook.com/BigRedConfessions/')
def topic_model(url):
  page_id_and_access_token = get_access_token_page_id(url)
  page_id = page_id_and_access_token[0]
  create_directory_for_topic_model(page_id)
  FileSplitter(page_id).split()
  lda_train = runR(page_id)
  lda_train.convert_to_matrix()
  lda_train.train_lda()

if __name__ == '__main__':
    cli()
