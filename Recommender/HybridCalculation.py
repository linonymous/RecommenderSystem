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

def hybrid(a, b):
    """
        hybrid calculation of ratings
    """
    c = {}
    alpha = 1/5
    beta = 5/6
    for user in a:
        for item in b:
            if user not in c.keys():
                c[user] = []
            if item in b.keys() and user in b[item]:
                u_i = b[item][user]
                u_u = a[user][item]
            elif item in b.keys() and user not in b[item]:
                u_i = 0
                u_u = a[user][item]
            elif item not in b.keys():
                continue
            rating = alpha *  u_u + beta * u_i
            c[user].append({item : rating})
        
        
def hybrid_runner():
    user = read_user_user()
    item = read_user_item()
    hybrid(user, item)