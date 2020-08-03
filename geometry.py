#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:26:00 2020

@author: max
"""
import numpy as np

def centroid(point_coords):
    
    '''
    Compute the centroid of a polygon
    https://en.wikipedia.org/wiki/Centroid#Of_a_polygon
    
    Input - numpy array of shape (N,2) of the N points of the polygon,
            first column are the x coordinates, second column the y coordinates
    Output - x and y coordinates of the centroid
    '''
    
    # Define x and y coordinates
    x_i = point_coords[:, 0]
    y_i = point_coords[:, 1]
    
    # coordinates of next point (looping over at the last point)
    x_i_plus_1 = np.concatenate((x_i[1:], np.expand_dims(x_i[0],axis=0)))
    y_i_plus_1 = np.concatenate((y_i[1:], np.expand_dims(y_i[0],axis=0)))
    
    # Term used in all lines below
    T = x_i*y_i_plus_1 - x_i_plus_1*y_i
    
    # Compute area
    A = 0.5 * np.sum(T)
    
    # Compute coordinates of centroid
    Cx = 1/(6*A) * np.sum((x_i + x_i_plus_1) * T)
    Cy = 1/(6*A) * np.sum((y_i + y_i_plus_1) * T)
    
    return Cx, Cy