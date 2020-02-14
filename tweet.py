import tweepy
import logging

class tweet():
    logger = logging.getLogger(__name__)
    def __init__(self, config):
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(
            config["TWITTER_CONSUMER_KEY"],
            config["TWITER_CONSUMER_SECRET"]
        )
        
        auth.set_access_token(config["TWITER_ACCESS_TOKEN"], config["TWITER_ ACCESS_TOKEN_SECRET"])
        
        # Create API object
        self.api = tweepy.API(auth)
        
        try:
            self.api.verify_credentials()
            self.connected = True
            logging.info('Connection Twitter OK')
        except:
            self.connected = False
            logging.info('Echec de connection a twitter')

    def send_post(self, post):
        """send_post"""
        if self.connected == True:
            try:
                # Create a tweet
                self.api.update_status("\
                Hello les twittos, un nouvel article\n %s\
                "%(post['status']))
                logging.info('Twitter post OK')
            except:
                logging.info("Tweetpy Error during post")
                logging.info('Twitter post : %s' % (post['status']))
                return 1
        else:
            logging.info('Echec de connexion twitter' )
            return 1
            
        
