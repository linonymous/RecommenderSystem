# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 12:21:39 2017

@author: Swapnil.Walke
"""
import numpy as np
import pandas as pd
from LinearRegression.LinearRegression import LinearRegression

data = pd.read_csv('book.csv')
x_df = pd.DataFrame(data.x)
y_df = pd.DataFrame(data.y)
print data.head()
print x_df
print y_df
train_x = x_df.iloc[:2]
train_y = y_df.iloc[:2]

test_x = x_df.iloc[:2]
test_y = y_df.iloc[:2]

model = LinearRegression()
model.train(train_x, train_y, 0.001, 2000)
print model.test(test_x, test_y)
print model.predict(21)
print model.theta
"""
points = points[1:]
train_set = points[:16]
test_set = points[-4:]

print "test" 
print test_set
print "train"
print train_set

model = LinearRegression()

model.train(train_set, 0.0000001, 100)
val = model.test(train_set)
print "Prediction" + str(model.predict(21))
#for x in points[1:]:
 #   print str(x[0]) + " "+ str(x[1])"""