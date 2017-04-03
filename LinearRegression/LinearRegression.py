# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 16:13:08 2017

@author: Swapnil.Walke
"""

import numpy as np
import pandas as pd
class LinearRegression:
    
    def __init__(self):
        self.theta = np.array([0, 0])
        self.iterations = 0
        self.learning_rate = 0
    
    def cost_function(self, X, y, theta):
        """
                cost_function(X, y, theta) computes the cost of using theta as the
                 parameter for linear regression to fit the data points in X and y
        """
        # number of training examples
        m = len(y)
        # Calculate the cost with the given parameters
        J = np.sum((X.dot(theta) - y) **2)/2/m
        return J


    def gradient_descent(self, X, y, theta, learning_rate, iterations):
        """
        gradient_descent Performs gradient descent to learn theta
        theta = GRADIENTDESENT(X, y, theta, learning_rate, num_iters) updates theta by 
        taking num_iters gradient steps with learning rate learning_rate
        """
        m = len(y)
        cost_history = [0] * iterations
        for iteration in range(iterations):
            hypothesis = X.dot(theta)
            loss = hypothesis - y
            gradient = X.T.dot(loss)/m
            theta = theta - learning_rate/m * gradient
            cost = self.cost_function(X, y, theta)
            cost_history[iteration] = cost

        return theta, cost_history
    
    def train(self, X, y, learning_rate, iterations):
        
        self.learning_rate = learning_rate
        self.iterations = iterations
        X['intercept'] = pd.Series(1, index=X.index)
        #X.loc[:,'intercept'] = pd.Series(1, index=X.index)
        X = np.array(X)
        y = np.array(y).flatten()
        (t, c) = self.gradient_descent(X, y, self.theta, learning_rate, iterations)
        self.theta = t
    
    def predict(self, X):
        
        return np.array([X, 1]).dot(self.theta)
    
    def test(self, X, y):
        
        X.loc[:,'intercept'] = pd.Series(1, index=X.index)
        X = np.array(X)
        y = np.array(y).flatten()
        init_cost = self.cost_function(X, y, np.array([0, 0]))
        new_cost = self.cost_function(X, y, self.theta)
        return (new_cost / init_cost) * 100