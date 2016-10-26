import urllib2
import json
import datetime
import csv
import os
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)
 
class PostScraper(object):
    """docstring for ClassName"""
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        self.access_token = access_token
        
    def testFacebookPageData(self):
        page_id = self.page_id
        # construct the URL string
        base = "https://graph.facebook.com/v2.4"
        node = "/" + page_id
        parameters = "/?access_token=%s" % self.access_token
        url = base + node + parameters
        # retrieve data
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        print json.dumps(data, indent=4, sort_keys=True)

    def request_until_succeed(self, url):
        req = urllib2.Request(url)
        success = False
        while success is False:
            try: 
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    success = True
                    print 'success'
            except Exception, e:
                print e
                time.sleep(5)
                print "\nError for URL %s: %s" % (url, datetime.datetime.now())
        return response.read()

    def testFacebookPageFeedData(self):
        base = "https://graph.facebook.com/v2.4"
        node = "/" + self.page_id + "/feed" # changed
        parameters = "/?access_token=%s" % self.access_token
        url = base + node + parameters
        data = json.loads(request_until_succeed(url))
        print json.dumps(data, indent=4, sort_keys=True)
    
    def getFacebookPageFeedData(self, num_statuses):
        base = "https://graph.facebook.com"
        node = "/" + self.page_id + "/feed" 
        parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(100).summary(true),comments.limit(10).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, self.access_token) # changed
        url = base + node + parameters
        data = json.loads(self.request_until_succeed(url))
        return data
        
    def processFacebookPageFeedStatus(self, status):
        status_id = status['id']
        status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')
        link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
        status_type = status['type']
        status_link = '' if 'link' not in status.keys() else status['link']
        
        status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + datetime.timedelta(hours=-5) # EST
        status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
        num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
        num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
        blank = None
        try:
            num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
        except KeyError:
            num_comments = 0

        return (status_id, status_message, link_name, status_type, status_link,
               status_published, num_likes, num_comments, num_shares)


    def scrapeFacebookPageFeedStatus(self):
        with open('../data/%s_output/%s_FBScraper_Posts.csv' % (self.page_id, self.page_id), 'wb') as file:
            w = csv.writer(file)
            w.writerow(["status_id", "status_message", "link_name", "status_type", "status_link",
               "status_published", "num_likes", "num_comments", "num_shares"])

            has_next_page = True
            num_processed = 0   # keep a count on how many we've processed
            scrape_starttime = datetime.datetime.now()
            
            print "\nScraping %s Facebook Page: %s\n" % (self.page_id, scrape_starttime)
            
            statuses = self.getFacebookPageFeedData(100)
            
            while has_next_page:
                for status in statuses['data']:
                    w.writerow(self.processFacebookPageFeedStatus(status))
                    # output progress occasionally to make sure code is not stalling
                    num_processed += 1
                    if num_processed % 1000 == 0:
                        print "%s Statuses Processed: %s" % (num_processed, datetime.datetime.now())
                # if there is no next page, we're done.
                if 'paging' in statuses.keys():
                    statuses = json.loads(self.request_until_succeed(statuses['paging']['next']))
                else:
                    has_next_page = False        
            print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)

