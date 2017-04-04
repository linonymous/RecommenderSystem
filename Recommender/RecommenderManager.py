# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 15:41:09 2017

@author: Swapnil.Walke
"""
from math import sqrt
import logging
import pandas as pd
from Log.log import Log
from LinearRegression.LinearRegression import LinearRegression

class RecommenderManager:
    
    def __init__(self):
        log = Log('C:\\Users\\Swapnil.Walke\\RecommenderSystem\\Log\\recommender.log')
        self.logger = logging.getLogger()
        self.logger.info('RecommenderManager object created.')
        
    def init(self, filename):
        logger.info('reading csv file...')
        df = pd.read_csv(filename)
        d = {}
        cnt = 0
        for index, row in df.iterrows():
            if row['userId'] not in d.keys():
                d[row['userId']] = {}
                d[row['userId']][row['movieId']] = row['rating']
            else:
                d[row['userId']][row['movieId']] = row['rating']
            cnt += 1
            if cnt == 1000:
                break
        return d
    
    def train_model(self, prefs, user1, user2):
        si={}
        rat1 = []
        rat2 = []
        for item in prefs[user1]:
            if item in prefs[user2]: 
                si[item]=1
                rat1.append( prefs[user1][item] )
                rat2.append( prefs[user2][item] )
        n = len(si)
        d = {}
        d['x'] = pd.Series( rat1 )
        d['y'] = pd.Series( rat2 )
        df = pd.DataFrame(data = d, columns = ['x', 'y'])
        x_df = pd.DataFrame( df.x )
        y_df = pd.DataFrame( df.y )
        model = LinearRegression()
        model.train(x_df, y_df, 0.001, 2000)
        self.logger.info('training_model')
        return model
    
    def sim_pearson(self, prefs, p1, p2):
    # Get the list of mutually rated items
        si={}
        for item in prefs[p1]:
            if item in prefs[p2]:
                si[item]=1
        # Find the number of elements
        n=len(si)
        # if they are no ratings in common, return 0
        if n==0: 
            return 0
        # Add up all the preferences
        sum1=sum([prefs[p1][it] for it in si])
        sum2=sum([prefs[p2][it] for it in si])
        # Sum up the squares
        sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
        sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
        # Sum up the products
        pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
        # Calculate Pearson score
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0: return 0
        r=num/float(den)
        return r
    
    # Gets recommendations for a person by using a weighted average
    # of every other user's rankings
    def getRecommendations(self, prefs, person):
        totals={}
        simSums={}
        for other in prefs:
            # don't compare me to myself
            if other == person: continue
            sim = self.sim_pearson(prefs,person,other)
            # ignore scores of zero or lower
            if sim<=0: continue
            for item in prefs[other]:
                # only score items I haven't seen yet
                if item not in prefs[person] or prefs[person][item]==0:
                    # Similarity * Score
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item]*sim
                    # Sum of similarities
                    simSums.setdefault(item,0)
                    simSums[item]+=sim
        # Create the normalized list
        rankings=[(total/simSums[item],item) for item,total in totals.items( )]
        # Return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings
    
    def transformPrefs(self, prefs):
        result={}
        for person in prefs:
            for item in prefs[person]:
                result.setdefault(item,{})
                # Flip item and person
                result[item][person]=prefs[person][item]
        return result
    
if __name__ == '__main__':
    obj = RecommenderManager()
    a = obj.init('C:\\Users\\Swapnil.Walke\\RecommenderSystem\\Dataset\\new.csv')
    k = 'Four Weddings and a Funeral (1994)'
    j = 'Birdcage, The (1996)'
    a = obj.transformPrefs(a)
    print a
    obj.sim_pearson(a, k, j)
    #print a
    print len(a)
    logging.info('2nd time I am doing this')
    print obj.getRecommendations(a, 'Birdcage, The (1996)')
    logging.info('3rd time I am doing this')