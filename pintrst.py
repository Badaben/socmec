import pinterest
import logging

class mypint():
    logger = logging.getLogger(__name__)
    def __init__(self, config):
        # Generate OAuth2 authorization link
        #link = pinterest.oauth2.authorization_url(self.config['PINTEREST_APP_ID'], self.config['PINTEREST_REDIRECT_URI'])
        try:
            self.api = pinterest.Pinterest(token=self.config['PINTEREST_AUTH_TOKEN'])
            self.connected = True
            logging.info('pinterest connected')
        except:
            self.connected = False
            logging.info('Echec de connection a pinterest')
        pass
        
    def send_post(self, post):
        
        logging.info(
        "Pinterest post : board = %s note = %s\
        link = %s image_url = %s" % (
                post['board'],
                post['note'],
                post['link'],
                post['image_url']
            )
        )

        
        if self.connected == True:
            self.api.pin().create(post['board'], post['note'], post['link'], image_url=post['image_url'])
        else:
            logging.info('Echec de la connection a Pinterest')
        
        
#        # Generate OAuth2 authorization link
#        link = pinterest.oauth2.authorization_url(app_id, redirect_uri)
#
#        # Initialize API by passing OAuth2 token
#        api = pinterest.Pinterest(token="ApFF9WBrjug_xhJPsETri2jp9pxgFVQfZNayykxFOjJQhWAw")
#
#        # Fetch authenticated user's data
#        api.me()
#
#        # Fetch authenticated user's boards
#        api.boards()
#        
#        # Create a pin
#        api.pin().create(board, note, link, image_url=image_url)
