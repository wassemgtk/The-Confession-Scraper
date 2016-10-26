#!/usr/bin/python
# -*- coding: <utf-8> -*-
import subprocess
import os

class runR(object):
  """docstring for runR"""
  def __init__(self, page_id):
    self.page_id = page_id
  
  def convert_to_matrix(self):
    page_ids = self.page_id
    ouput = '%s_output' % self.page_id
    posts_split = '%s_posts_split'  % self.page_id
    matrix = '%s_lda_matrix.RData' % self.page_id

    # Define command and arguments
    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), "convert_to_matrix.R")
    # Variable number of args in a list
    # Build subprocess command
    cmd = [command, path2script, page_ids, ouput, posts_split, matrix] 

    x = subprocess.check_output(cmd)
    print x

  def train_lda(self):
    ouput = '%s_output' % self.page_id
    matrix = '%s_lda_matrix.RData' % self.page_id
    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), "lda_model.R")
    # Variable number of args in a list
    # Build subprocess command
    cmd = [command, path2script, ouput, matrix] 

    x = subprocess.check_output(cmd)
    print x


