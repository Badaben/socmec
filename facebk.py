import facebook
import logging
import requests
import json


class facebk():
    logger = logging.getLogger(__name__)
    def __init__(self, config):
        FACEBOOK_ACCESS_TOKEN = self.tokens()
        self.graph = facebook.GraphAPI( access_token=FACEBOOK_ACCESS_TOKEN)

        try:
            self.me = self.graph.get_object('me')
            pages = self.graph.get_object('cotesmeubles')
            logging.info('Connected as : %s id : %s' % (str(self.me['name']), str(self.me['id'])))
            self.connected = True
        except:
            logging.info('Echec de connection a facebook')
            self.connected = False
        pass
    
    def tokens(self):
   
        # open json file for reading
        with open('conf/facebook.json', 'r') as f:
            data = json.load(f)

        # read user info
        user_short_token = data['user']['short_token']
        user_long_token = data['user']['long_token']

        # read app info
        app_id = data['app']['id']
        app_secret = data['app']['secret']

        # read page info
        page_token = data['page']['token']
        page_id = data['page']['id']

        host = "https://graph.facebook.com"
        endpoint = "/oauth/access_token"

        # get first long-lived user token
        if user_long_token == 'None':
            user_long_token = requests.get(
                "{}{}?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(
                    host, endpoint, app_id, app_secret, user_short_token)).json()['access_token']

            # update value
            data['user']['long_token'] = user_long_token
            
            # get first permanent page token
            graph = facebook.GraphAPI(access_token=user_long_token, version="3.1")
            pages_data = graph.get_object("/me/accounts")

            for item in pages_data['data']:
                if item['id'] == page_id:
                    page_token = item['access_token']

            # update value
            data['page']['token'] = page_token

        # use stored permanent page token to request a new one
        else:
            page_token = requests.get(
                "{}{}?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(
                        host, endpoint, app_id, app_secret, page_token)).json()['access_token']

            # update value
            data['page']['token'] = page_token

        # open json file for writing
        with open('conf/facebook.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return data['page']['token']

    
        
    def send_post(self, post):
        
        logging.info("Facebook post : message = %s link = %s" % (post['message'], post['link']))
        
        if self.connected == True:
            
            self.graph.put_object(
               parent_object="me",
               connection_name="feed",
               message=post['message'],
               link=post['link'])
        else:            logging.info('Echec de connexion a Facebook')

