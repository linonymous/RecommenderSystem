# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 14:54:01 2017

@author: Swapnil.Walke
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('book.csv')
print data

## Split population and profit into X and y
X_df = pd.DataFrame(data.x)
y_df = pd.DataFrame(data.y)

#print X_df['x']
#pd.to_numeric(X_df['x'])
#X_df = X_df.convert_objects(convert_numeric=True)
#y_df = y_df.convert_objects(convert_numeric=True)
## Length, or number of observations, in our data
m = len(y_df)
"""
plt.figure(figsize=(10,8))
plt.plot(X_df, y_df, 'kx')
plt.xlabel('Population of City in 10,000s')
plt.ylabel('Profit in $10,000s')


plt.figure(figsize=(10,8))
plt.plot(X_df, y_df, 'k.')
plt.plot([5, 22], [6,6], '-')
plt.plot([5, 22], [0,20], '-')
plt.plot([5, 15], [-5,25], '-')"""

iterations = 1500
alpha = 0.01

## Add a columns of 1s as intercept to X
X_df['intercept'] = 1

## Transform to Numpy arrays for easier matrix math and start theta at 0
X = np.array(X_df)
y = np.array(y_df).flatten()
theta = np.array([0, 0])

def cost_function(X, y, theta):
    """
    cost_function(X, y, theta) computes the cost of using theta as the
    parameter for linear regression to fit the data points in X and y
    """
    ## number of training examples
    m = len(y) 
    
    ## Calculate the cost with the given parameters
    h = (X.dot(theta)-y)
    J = np.sum(h **2)/2/m
    
    return J

print cost_function(X, y, theta)

def gradient_descent(X, y, theta, alpha, iterations):
    """
    gradient_descent Performs gradient descent to learn theta
    theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
    taking num_iters gradient steps with learning rate alpha
    """
    cost_history = [0] * iterations
    
    for iteration in range(iterations):
        hypothesis = X.dot(theta)
        loss = hypothesis-y
        gradient = X.T.dot(loss)/m
        print theta
        print gradient
        break
        theta = theta - alpha*gradient
        cost = cost_function(X, y, theta)
        cost_history[iteration] = cost

    return theta, cost_history

(t, c) = gradient_descent(X, y, theta, alpha, iterations)
print t
print np.array([21, 1]).dot(t)
print cost_function(X, y, t)