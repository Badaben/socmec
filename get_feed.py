import feedparser
import os 
import json
import logging

class feeder():
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.lockfile = 'lockfile.json'
        self.log_dir =''
        
        # for test remove the state file
        if os.path.isfile(self.lockfile):
            os.remove(self.lockfile)
        pass
    
    def get_feed(self, url):
        
        d = feedparser.parse(url)
        
        if d['entries'][0]:
            post = { 
                'title' :  d['entries'][0]['title'], 
                'url' :   d['entries'][0]['link'], 
                'img' :  d['entries'][0]['links'][0]['href'], 
                'description' : d['entries'][0]['description']
                }
        else:
            post = {
                'title' :  '', 
                'url' :   '', 
                'img' :  '', 
                'description' : ''
            }
            
        return post
    
    def get_lock(self, lock):
        
        if os.path.isfile(lock):
            
            with open(lock, 'r') as f:
                last = json.load(f)
                return last
            
        else:
            last = {
                'title' : '', 
                'url' : '', 
                'img' : '', 
                'description' : ''            
            }
            return last

    def compare_feed(self, post, last):
        
        if  post['url'] == last['url'] :
            # Déja publié
            #print("1 : %s ----- 2 : %s"%(post['url'], last['url']))
            return 'PUBLISHED'
        else:
            # Nouveau post on met a jour le fichier lock et on pousse le post
            with open(self.lockfile, 'w') as f:
                f.write(json.dumps(post, indent=4))
            return post

    def run_it(self, url):
        
        feed = self.get_feed(url)
        if feed['title'] != '':
            last = self.get_lock(self.lockfile)
            post = self.compare_feed(feed, last)
            return post
        else:
            #print('feed is empty')
            return 'EMPTY'
