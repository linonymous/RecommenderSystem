# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 15:45:36 2017

@author: Swapnil.Walke
"""

import logging

class Log:
    
    def __init__(self, file_name):
        
        logger = logging.getLogger()
        LOG_FILENAME = file_name
        ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000000, backupCount=15)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)