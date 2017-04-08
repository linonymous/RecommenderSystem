# -*- coding: utf-8 -*-
"""
Created on Sun Apr 02 12:01:59 2017

@author: Swapnil.Walke
"""
import json
import pandas as pd
import numpy as np
from math import sqrt
from LinearRegression.LinearRegression import LinearRegression
import logging
logger = logging.getLogger()
LOG_FILENAME = 'temp.log'
ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000000, backupCount=15)

        # Uncomment this if you want console logging or file logging
        # ch = logging.StreamHandler()
        # ch = logging.FileHandler("log/log.0")

ch.setLevel(logging.DEBUG)

        # create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
ch.setFormatter(formatter)

        # add ch to logger
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)
#logger = logging.
#logging.basicConfig(filename = 'temp.log')
#logging.info('its working fine...')
df = pd.read_csv('new.csv')

def init():
    d = {}
    cnt = 0
    for index, row in df.iterrows():
        if row['userId'] not in d.keys():
            d[row['userId']] = {}
            d[row['userId']][row['movieId']] = row['rating']
        else:
            d[row['userId']][row['movieId']] = row['rating']
        cnt += 1
        if cnt == 100000:
            break
    return d


def sim_pearson(prefs,p1,p2):
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


def train_model(prefs, user1, user2):
    si={}
    rat1 = []
    rat2 = []
    for item in prefs[user1]:
        if item in prefs[user2]: 
            si[item]=1
            rat1.append( prefs[user1][item] )
            rat2.append( prefs[user2][item] )
    #print si.keys()
    n = len(si)
    d = {}
    d['x'] = pd.Series( rat1 )
    d['y'] = pd.Series( rat2 )
    df = pd.DataFrame(data = d, columns = ['x', 'y'])
    x_df = pd.DataFrame( df.x )
    y_df = pd.DataFrame( df.y )
    model = LinearRegression()
    model.train(x_df, y_df, 0.001, 1800)
    return model
    

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    with open('user-user-model.json') as data_file:    
        data = json.load(data_file)
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs,person,other)
        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:
            # only score items I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
            # Similarity * Score
                totals.setdefault(item,0)
        #        model = train_model(prefs, other, person)
         #       rating = model.predict(prefs[other][item])
                #print str(person) + " " + str(other)
                if str(other) in data.keys():
                    rating = np.array([prefs[other][item], 1]).dot(data[str(other)][str(person)])
                else:
                    rating = prefs[other][item]
                totals[item]+= rating * sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total / simSums[item], item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

a = init()
a = transformPrefs(a)
#print getRecommendations(a, 1 )
#a = transformPrefs(a)
#print sim_pearson(a, 'Four Weddings and a Funeral (1994)', 'Birdcage, The (1996)' )

#print a
print len(a)

#logging.info('2nd time I am doing this')


user = {}
def write(data):
    with open('user-user-model.json', 'w') as f:
        json.dump(data, f)
        
for i in range (1, len(a)):
    for j in range(1, len(a)):
        if i == j: 
            continue
        sim = sim_pearson(a, i, j)
        if sim<= 0: 
            continue
        model = train_model(a, i, j)
        print str(i) + " " + str(j) + str(model.theta)
        if i not in user.keys():
            user[i] = {}
        ls = []
        ls.append(model.theta[0])
        ls.append(model.theta[1])
        user[i][j] = ls
    if i%50 == 0:
        write(user)
        
with open('user-item-model.json') as data_file:    
    data = json.load(data_file)

"""
user[1] = {}
model = train_model(a, 1, 2)



ls = []
ls.append(model.theta[0])
ls.append(model.theta[1])
user[1][2] = ls
d = {}
for i in range(1, len):
    b = getRecommendations(a, i)
    d[i] = []
    ite = {}
    for rating, item in b:
        ite[item] = rating
    d[i].append(ite)
    print i
with open('user-item.json', 'w') as f:
    json.dump(d, f)
logging.info('2nd time I am doing this')
#print sim_pearson(a, 1, 19)
#print a"""