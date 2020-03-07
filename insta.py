#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import logging

class myinsta():
    logger = logging.getLogger(__name__)
    def __init__(self, config):
        from InstagramAPI import InstagramAPI
        try:
            self.InstagramAPI = InstagramAPI(config['INSTAGRAM_LOGIN'], config['INSTAGRAM_PASSWORD'])
            self.InstagramAPI.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
            con = self.InstagramAPI.login()  # login
            if con == True:
                logging.info('Connection a Instagram Ok ')
                self.connected = True
                
            else:
                logging.info('Echec de connection a Instagram :%s' % (con['error_type']))
                self.connected = False
        except:
            logging.info('Erreur ')
            self.connected = False

        
    def send_post(self, post):
        
        logging.info("Instagram post : photo_path = %s caption = %s" % (post['photo_path'], post['caption']))
        if self.connected == True:
            self.InstagramAPI.uploadPhoto(post['photo_path'],  caption=post['caption'])
        else:
            logging.info('Echec de connexion Instagram')
        
        return
