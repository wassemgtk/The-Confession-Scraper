import urllib2
import json
import datetime
import csv # Unused import csv
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)
 
class CommentScraper(object):
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

    def request_until_succeed(self, url): # Method could be a function (when there is no reference to the class, suggesting that the method could be used as a static function instead If the class method )
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
                print "Error for URL %s: %s" % (url, datetime.datetime.now())
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
        
    def processFacebookPageFeedStatus(self, status): # Method could be a function 
        status_id = status['id'] # Unused variable 'status_id'

        try:
            num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count'] # Unused variable 'num_comments'
        except KeyError:
            num_comments = 0
            print 'COMMENTS FAILS'

        try:
            if status['comments']['summary']['total_count'] == 0:
                comment_id = 0 # Unused variable 'comment_id'
                comment_message = 0
                comment_author = 0 # Unused variable 'comment_author'
                comment_published= 0
            else:
                # with open('../output/%s_facebookScraper_Comments.csv' % self.page_id, 'wb') as file:
                print "NEEEW"

                for i in range(len(status['comments']['data'])):
                    print 'count' + str(status['comments']['summary']['total_count'])
                    print i
                    # pp.pprint(status['comments']['data'][i]['message'])
                    # w = csv.writer(file)
                    # w.writerow(['status_id', 'num_comments', 'comment_id', 'comment_message', 'comment_author', 'comment_published'])
                    comment_published = datetime.datetime.strptime(status['comments']['data'][i]['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
                    comment_message  = '' if 'message' not in status['comments']['data'][i].keys() else status['comments']['data'][0]['message'].encode('utf-8')
                    comment_author = '' if 'from' not in status['comments']['data'][i].keys() else status['comments']['data'][0]['from']
                    comment_id = '' if 'id' not in status['comments']['data'][i].keys() else status['comments']['data'][0]['id']
                    comment_published = comment_published + datetime.timedelta(hours=-5) # EST
                    comment_published = comment_published.strftime('%Y-%m-%d %H:%M:%S')
                    print comment_message
                    # w.writerow([status_id, num_comments, comment_id, comment_message, comment_author, comment_published])
        except KeyError:
            comment_id = None
            comment_message = None
            comment_author = None
            comment_published= None
            print 'COMMENTS FAILS'

    def scrapeFacebookPageFeedStatus(self):
        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        print "Scraping %s Facebook Page: %s\n" % (self.page_id, scrape_starttime)
        statuses = self.getFacebookPageFeedData(100)
        
        while has_next_page:
            for status in statuses['data']:
                self.processFacebookPageFeedStatus(status)
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

