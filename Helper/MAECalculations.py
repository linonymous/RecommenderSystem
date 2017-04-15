# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:21:56 2017

@author: Swapnil.Walke
"""

import json
import pandas as pd
import numpy as np
from math import sqrt

def init():
    df = pd.read_csv('new.csv')
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

def read_uu():
    with open('user-user-model.json') as data_file:    
        data = json.load(data_file)
    return data

def read_ui():
    with open('user-item-model.json') as data_file:    
        data = json.load(data_file)
    return data
    
def similarity(prefs, p1, p2):
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
        num=pSum-(sum1 * sum2/n)
        den=sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))
        if den==0: return 0
        r=num/float(den)
        return r
    

def calculate_MSE_UU(prefs, person):
    data = read_uu()
    err = 0
    cnt = 0
    for item in prefs[person]:
        num = 0.0
        den = 0.0
        for other in prefs:
            if other == person:
                continue
            if item not in prefs[other]:
                continue
            sim = similarity(prefs, other, person)
            if sim <= 0:
                continue
            if str(other) not in data.keys():
                continue
            """
            print other
            print item
            print prefs[other][item]
            print data[str(other)][str(person)]"""
            rating = np.array([prefs[other][item], 1]).dot(data[str(other)][str(person)])
            num += rating * sim
            den += sim
        #print num
        #print den
        if den <= 0:
            continue
        pred = num / float(den)
        err += (pred - prefs[person][item]) ** 2
        cnt = cnt + 1
    return err, cnt

def transformPrefs( prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

def init_hybrid():
    with open('rating.json') as data_file:    
        data = json.load(data_file)
    users = {}
    for user in data:
        if user not in users.keys():
            users[user] = {}
        for item in data[user]:
            users[user].update(item)
    return users



def calculate_MSE_hy(prefs, aprefs, person):
    data_uu = read_uu()
    data_ui = read_ui()
    err = 0
    cnt = 0
    for item_a in prefs[person]:
        num_uu = 0.0
        den_uu = 0.0
        
        for other in prefs:
            try:
                if person == other:
                    continue
                if item_a not in prefs[other]:
                    continue
                sim = similarity ( prefs, other, person)
                if sim <= 0:
                    continue
                if str(other) not in data_uu.keys():
                    continue
                rating = np.array([prefs[other][item_a], 1]).dot(data_uu[str(other)][str(person)])
                num_uu += rating * sim
                den_uu += sim
            except UnicodeDecodeError:
                continue
        if den_uu <= 0:
            continue
        pred_uu = num_uu / float(den_uu)
        num_ui = 0.0
        den_ui = 0.0
        for item_b in data_ui.keys():
            try:
                if item_a == item_b:
                    continue
                sim = similarity(aprefs, str(item_a.encode('utf-8')), str(item_b.encode('utf-8')))
                if sim<= 0:
                    continue
                if item_b not in data_ui.keys():
                    continue
                rating = np.array([aprefs[item_a][person], 1]).dot(data_ui[item_b][item_a])
                num_ui += rating * sim
                den_ui += sim
            except UnicodeDecodeError:
                continue
        if den_ui <= 0:
            continue
        pred_ui = num_ui / float(den_ui)
        pred = ((1/6.0) * pred_uu) + ((5/6.0) * pred_ui)
        err += ( (prefs[person][item_a] - pred) / prefs[person][item_a]) ** 2
        cnt += 1
        print cnt
        if cnt > 5000:
            break
    return cnt, err
    

a = init()
aprefs = transformPrefs(a)
count = 0
error = 0
i = 1
while count<5000:
    i = i + 1
    cnt, err = calculate_MSE_hy(a, aprefs, i)
    error += err
    count += cnt
    print count
    if count > 5000:
        break
print error #error 394.030884673
print count #count 1926"""
print error/count
"""1246.35525219
5709
0.218314109684"""
#data = read_ui()
#print data.keys()[:3]
#print a[199].keys()

#data = init_hybrid()
#print a[int(str(data.keys()[0]))].keys()
#print a[int(str(data.keys()[0]))].keys()
#a = init()
#err, cnt = calculate_MSE_UU(a, 1)
#print err
#print cnt
"""
i = 1
c = 0
error = 0
for count in range(0, 100):
    print i
    print c
    err, cnt = calculate_MAE_UU(a, i)
    i = i + 1
    error = error + err
    c += cnt
    if c > 100:
        break
    
print error
print c"""