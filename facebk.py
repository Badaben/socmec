import facebook
import logging

class facebk():
    logger = logging.getLogger(__name__)
    def __init__(self, config):
        self.graph = facebook.GraphAPI(
            access_token=config['FACEBOOK_ACCESS_TOKEN']
        )
        try:
            self.graph.get_object('me')
            self.connected = True
        except:
            logging.info('Echec de connection a facebook')
            self.connected = False
        pass
        
    def send_post(self, post):
        
        logging.info("Facebook post : message = %s link = %s" % (post['message'], post['link']))
        
        if self.connected == True:
            
            self.graph.put_object(
               parent_object="me",
               connection_name="feed",
               message=post['message'],
               link=post['link'])
        else:
            logging.info('Echec de connexion a Facebook')

