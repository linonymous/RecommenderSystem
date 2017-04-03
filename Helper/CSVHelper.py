# -*- coding: utf-8 -*-
"""
Created on Sun Apr 02 09:27:37 2017

@author: Swapnil.Walke
"""

import pandas as pd
import numpy as np
import logging  
logging.basicConfig(filename = 'CSVHelper.log')

class CSVHelper:
    
    def __init__(self):
        logging.info('CSVHelper class obj created.')

    def read_data(self, filename):
    
        df = pd.read_csv(filename, delimiter=',')        