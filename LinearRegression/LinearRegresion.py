# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 11:06:57 2017

@author: Swapnil.Walke
"""

import numpy as np

class LinearRegression:
    
    def __init__(self):
        
        self.learning_rate = 0
        self.initial_b = 0
        self.initial_m = 0
        self.num_iterations = 0
        self.final_b = 0
        self.final_m = 0
    
    
    def validation(self, b, m, points):
        
        total_error = 0
        for i in range(0, len(points)):
            x = points[i, 0]
            y = points[i, 1]
            total_error += (y - ( (m * x) + b) ) **2
        return total_error/float(len(points))
    
    
    def gradient_descent_runner(self, points, starting_b = None, starting_m = None, learning_rate = None, num_iterations = None):
        
        if starting_b == None:
            starting_b = self.initial_b
        if starting_m == None:
            starting_m = self.initial_m
        if learning_rate == None:
            learning_rate = self.learning_rate
        if num_iterations == None:
            num_iterations = self.num_iterations
        b = starting_b
        m = starting_m
    
        for i in range(num_iterations):
            b, m = self.step_gradient(b, m, np.array(points), learning_rate)
    
        return [b, m]
    
    
    def step_gradient(self, b_current, m_current, points, learning_rate):
    
        b_gradient = 0
        m_gradient = 0
        n = float(len(points))
        for i in range(0, len(points)):
            x = points[i, 0]
            y = points[i, 1]
            # direction with respect to b and m
            b_gradient += -(2/n) * (y - ((m_current * x) + b_current))
            m_gradient += (2/n) * x * (y - ((m_current * x) + b_current))
        
        new_b = b_current - (learning_rate * b_gradient)
        new_m = m_current - (learning_rate * m_gradient)

        return [new_b, new_m]
    
    def train(self, points, learning_rate, num_iterations):
        
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.points = points
        [b, m] = self.gradient_descent_runner(self.points, self.initial_b, self.initial_m, self.learning_rate, self.num_iterations)
        params = [b, m]
        self.final_b = params[0]
        self.final_m = params[1]
        return [b, m]
    
    def test(self, points):
        
        m = self.final_m
        b = self.final_b
        init_error = validation(self.initial_b, self.initial_m, points)
        new_error = validation(b, m, points)
        valid = 100 - (new_error/init_error) * 100 
        if valid <= 0:
            return 0
        else:
            return valid
    
    
        
        
        