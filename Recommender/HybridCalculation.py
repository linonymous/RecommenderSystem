# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 20:24:24 2017

@author: Swapnil.Walke
"""
import json

def read_user_user():
    with open('user-user.json') as data_file:    
        data = json.load(data_file)
    return data

def read_user_item():
    with open('user-item.json') as data_file:    
        data = json.load(data_file)
    return data

def write_final(d):
    with open('rating.json', 'w') as f:
        json.dump(d, f)
        
def hybrid(a, b):
    """
        hybrid calculation of ratings
    """
    c = {}
    alpha = 1/float(6)
    beta = 5/float(6)
    i = 0
    cnt = 0
    #print a.keys()
    for user in a:
        i += 1
        for item in b:
            #print user
            #print item
            if user not in c.keys():
                c[user] = []
            if item in b.keys() and item in a[user][0].keys() and user in b[item][0].keys():
                u_i = b[item][0][user]
                u_u = a[user][0][item]
                cnt += 1
            elif item in b.keys() and user not in b[item][0].keys() and item in a[user][0].keys():
                u_i = 0
                u_u = a[user][0][item]
            elif item not in b.keys() or item not in a[user][0].keys():
                continue
            #rating = max(u_u , u_i)
            #print 1/float(6) * u_u
            #print u_i
            #print 5/float(6) * u_i
            #print 
            rating = alpha *  u_u + beta * u_i
            #print rating
            #break
            c[user].append({item : rating})
        print i
        print "cnt " + str(cnt)
        #break
        if i % 15 == 0:
            write_final(c)
        
def hybrid_runner():
    users = read_user_user()
    items = read_user_item()
    #print users["1"][0]["Iron Giant, The (1999)"]
    #print items["Iron Giant, The (1999)"][0]["1"]
    """
    d = {}
    #print users['1'][0]
    for user in users:
        if user not in d.keys():
            d[user] = {}
        for item in users[user][0]:
            print item
            print users[user][0][item]
            break
        break
    #print user['1']['Little Big League (1994)']
    #print item['Iron Giant, The (1999)']"""
    hybrid(users, items)
    
hybrid_runner()