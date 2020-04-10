import json
import logging
import os
import sys
import time
import pathlib
from lxml import html

import facebk
import get_feed
from insta import myinsta
import pintrst
import tweet


class Beep():
    
    def __init__(self):
    
        try:
            conffile = os.path.join('conf', 'config.json')
            with open(conffile) as config_file:
                self.config = json.load(config_file)
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(module)s  %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                handlers=[
                    logging.FileHandler(self.config['paths']['log_file']),
                    logging.StreamHandler(sys.stdout)
                ]
            )
        except:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(module)s  %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                handlers=[
                    logging.StreamHandler(sys.stdout)
                ]
            )
            
            base_dir =  pathlib.Path.cwd()
            self.config = { 
            'main' : {
                'rss_url' : "http://cotesmeubles.fr/feed.php", 
                'time_sleep' : 600,  
                'base_dir' : str(base_dir)
            }, 
            'paths' : {
                'conf_dir' : str(base_dir.joinpath('conf')), 
                'conf_file' : str(base_dir.joinpath('conf').joinpath('config.json')), 
                'log_dir' : str(base_dir.joinpath('log')),
                'log_file' :  str(base_dir.joinpath('log').joinpath('Beep.log')),
                'img_dir' : str(base_dir.joinpath('img'))
            }, 
            'twitter' : {
                "TWITTER_CONSUMER_KEY" : '', 
                "TWITTER_CONSUMER_SECRET" : '', 
                "TWITTER_ACCESS_TOKEN" : '', 
                "TWITTER_ACCESS_TOKEN_SECRET" : '', 
                "TWITTER_MESSAGE_HEAD" : '', 
                "TWITTER_MESSAGE_TAIL" : '', 
                "TWITTER_HASHTAGS" : ''
            }, 
            'instagram' : {
                'INSTAGRAM_LOGIN' : '', 
                'INSTAGRAM_PASSWORD' : '', 
                "INSTAGRAM_MESSAGE_HEAD" : '', 
                "INSTAGRAM_MESSAGE_TAIL" : '',                     
            }, 
            'facebook' : {
                "FACEBOOK_MESSAGE_HEAD" : '', 
                "FACEBOOK_MESSAGE_TAIL" : '',  
            }, 
            'pinterest' : {
                'PINTEREST_APP_ID' : '', 
                'PINTEREST_REDIRECT_URI' : '', 
                'PINTEREST_ACCESS_TOKEN' : '', 
                "PINTEREST_MESSAGE_HEAD" : '', 
                "PINTEREST_MESSAGE_TAIL" : '', 
            }
        }
            self.check_dirs(self.config)
            self.first_config(self.config)
            
        logging.info('Started')
        logging.info('Checking rss from %s' % (self.config['main']['rss_url']))
    
    def first_config(self, config):
        
        logging.info('First run, creating config file')
        
        
        print('Configuration manuelle du script\n\n')
        doit = input('\tVoulez vous configurer le script manuellement y/N ?\n\
        \t(Vous pouvez editer le fichier conf/config.json)')
        
        if doit == 'y|Y':
            for key in config.keys():
                
                if str(key) != 'path' and str(input('Configuration de %s y/N ?' % (key))) == 'y' :
                    for item in config[key].keys():
                        ret = str(input('%s (%s)'%(item, config[key][item])))
                        if ret != '':
                            config[key][item] = ret
        # check facebook config             
        # populate config file
        if not os.path.isfile('conf/facebook.json'):
            data = {
                "user": {
                    "short_token": "add this manually",
                    "long_token": "None"
                },
                "app": {
                    "id": "add this manually",
                    "secret": "add this manually"
                },
                "page": {
                    "token": "None",
                    "id": "add this manually"}
            }
            #write configuration
            with open('conf/facebook.json', 'w') as f:
                json.dump(data, f, indent=4)
            
        with open(config['paths']['conf_file'], 'w') as configfile:
            configfile.write(json.dumps(config, indent=4))
        
        self.config = config
        
        print('Exiting, next launche will use configuration files (you need to edit), if errors occurs check file conf/config.json')
        exit(0)    
    
    def check_dirs(self, config):
        
        for key in config['paths'].keys():
            if '_dir' in str(key):
                p = pathlib.Path(config['paths'][key])
                p.mkdir(parents=True, exist_ok=True)

    def strip_html(self, s):
        
        return html.fromstring(s).text_content()

    def get_image(self, img_url):
        
        import requests
        logging.info('Download image : %s' % (img_url))
        url = img_url
        page = requests.get(url)

        img_filename = os.path.split(url)[1]
        f_name = '{}'.format(img_filename)
        f_name = os.path.join(self.config['paths']['img_dir'], f_name)
        with open(f_name, 'wb') as f:
            f.write(page.content)
        logging.info('IMG filename : %s' % (f_name))
        logging.info('Img download complete')
        return f_name
    
    def format_post(self, post):
        
        logging.info('Formating post .....')
        img_path = self.get_image(post['img'])
        
        # Tweet
        desc = str(self.strip_html(post['description']))
        twitpost = {'status' : '%s\n\n%s\n%s\n%s\n%s\n%s' % (
            self.config['twitter']['TWITTER_MESSAGE_HEAD'], 
            post['title'],
            desc,
            post['url'],
            self.config['twitter']['TWITTER_MESSAGE_TAIL'],
            self.config['twitter']['TWITTER_HASHTAGS'],
            )
        }
        logging.info('twitter post : %s' % (str(twitpost)))
        
        # Insta
        instapost = { 
            'photo_path' : img_path,
            'caption' : '%s\n%s\n%s' % (
                self.config['instagram']['INSTAGRAM_MESSAGE_HEAD'],
                post['title'], 
                self.config['instagram']['INSTAGRAM_MESSAGE_TAIL']
            )
        }
        logging.info('Instagram post : %s' % (str(instapost)))
        
        # Facebook
        facebkpost = {
            'message' :  '%s\n%s\n%s\n%s\n%s'%(
                self.config['facebook']['FACEBOOK_MESSAGE_HEAD'],  
                post['title'],
                desc,
                post['url'],
                self.config['facebook']['FACEBOOK_MESSAGE_TAIL'] 
            ), 
            'link' : post['url']
        }
        logging.info('Facebook post : %s' % (str(facebkpost)))
        
        # pinterest
        pintpost = {
            'board' : 'Default', 
            'note' : post['title'], 
            'link': post['url'], 
            'image_url' : post['img'], 
        }
        logging.info('Pinterest post : %s' % (str(pintpost)))
        
        posts = {
            'twitpost' : twitpost, 
            'instapost' : instapost, 
            'facebkpost' : facebkpost,
            'pintpost' : pintpost 
            }
        
        logging.info('Formating done')
        return posts
        
        
    def send_post(self, post):
        t = tweet.tweet(self.config['twitter'])
        i =  myinsta(self.config['instagram'])
        fb = facebk.facebk(self.config['facebook'])
        p = pintrst.mypint(self.config['pinterest'])
        posts = self.format_post(post)
        
        dry = True
        
        if t.connected and i.connected and fb.connected and p.connected and dry == False:
            # Twitter
            twit = t.send_post(posts['twitpost'])
            # Insta
            insta = i.send_post(posts['instapost'])
            # Facebook
            facebook = fb.send_post(posts['facebkpost'])
            # Pinsterest
            pinterest = p.send_post(posts['pintpost'])
        elif dry == True:
            logging.info('Dry mode : t=%s i=%s f=%s p=%s' % (
                t.connected,
                i.connected,
                fb.connected,
                p.connected
                )
            )
        else:
            logging.info('Connection failed : t=%s i=%s f=%s p=%s' % (
                t.connected,
                i.connected,
                fb.connected,
                p.connected
                )
            )
            logging.info('Failed to connect to at least one social service\n\
            Please verify credentials configuration in config.json\n\
            and rerun this script')
            exit(0)
        
    def main(self):
        
        
        
        f = get_feed.feeder()
 
        while True:
            
            post = f.run_it(self.config['main']['rss_url'])
            if post == 'PUBLISHED' : 
                pass
            else:
                logging.info('New post found : %s' % (str(post['title'])))
                self.send_post(post)
            logging.info('waiting %d secondes to recheck'%(int(self.config['main']['time_sleep'])))
            time.sleep(int(self.config['main']['time_sleep']))
        

if __name__ == "__main__":
    
    b = Beep()
    b.main()

