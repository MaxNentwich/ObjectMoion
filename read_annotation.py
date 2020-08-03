#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:10:18 2020

@author: max
"""
###
# Read .json file of annotation coordinates and plot on frames 
###

# Load libraries
import json 
import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
# Custom function to compute centroid
import geometry

# Define frame rate for plotting
fr = 30

# Select range of frames to plot (be carefull not to make too large)
frame_range = np.arange(3000, 3100)

# Run setup file (contains data directories)
exec(open('setup_object_motion.py').read())

# Load all possible colors from matplotlib
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = list(colors.keys())

##### TO-Do #####
# Make a dictionary of all objects and assign a color to each
#####
    
# Random reshuffle of colors
np.random.seed(1)
idx = np.random.permutation(len(colors))
colors = [colors[i] for i in idx]

# Load all files 
annotion_files = sorted(glob.glob(f'{annot_dir}/{present_dir}/present_*.json'))
frames = sorted(glob.glob(f'{annot_dir}/{present_dir}/present_*.jpg'))

# Create figure
fig = plt.figure()

# Load the annotation data
for i in frame_range:
    
    with open(annotion_files[i]) as f:
      annotation = json.load(f)
      
    # Load the current frame
    frame = cv2.imread(frames[i])
    
    ##### TO-Do #####
    # Colors of frames are messed up
    #####
    
    # Clear figure
    fig.clear()
    
    # Plot frame
    plt.imshow(frame)
      
    ##### TO-Do #####
    # Select a specific object (e.g. faces)
    #####
    
    # Loop over all shapes in this frame 
    for shape in range(len(annotation['shapes'])):  
        
        # Convert coordinates of annotation to numpy array
        point_coords = np.asarray(annotation['shapes'][shape]['points'])
        
        # Compute centroid
        Cx, Cy = geometry.centroid(point_coords)
        
        # Plot outline of current object annotation on the frame
        plt.fill(point_coords[:,0], point_coords[:,1], \
                 facecolor='none', edgecolor=colors[shape])
        
        # Plot the centroid 
        plt.plot(Cx, Cy, marker='o', color=colors[shape], \
                 label=annotation['shapes'][shape]['label'])
        
        # Don't show axes
        plt.axis('off')
        
    # Show the legend
    plt.legend()
    
    # Make fullscreen
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    
    # Tile 
    plt.title(f'Frame {i}')
    
    # Show plot and pause
    plt.show()
    plt.pause(1/fr)