# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 01:53:58 2021

@author: justwah
"""

import re
import imagesize
import numpy as np
import math
from collections import Counter


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def getPrevailSize(filenames: list): #unit: pixel
    size_list = []
    for filename in filenames:
        size_list.append(imagesize.get(filename))
        if Counter(size_list).most_common()[0][1] < 20:
            print("Warning: possibly irregular image sizes")
    return Counter(size_list).most_common()[0][0] #tuple:(width, height)

def getLogThreshold(dim: int, base: float=20, sensitivity: float=100):
    # larger base, threshold grow slower as img_data.shape increase (curve flatter)
    # larger sensitivity, looser detection
    threshold = math.log(dim, base) * sensitivity
    return threshold

def isLineWhiteV(img_data: np.array, x: int, base: float=20, sensitivity: float=100): # to avoid cutting words #maybe better count non-white point but more computation?
    # no. of point < inverse sen : threshold = no. of point
    # no. of point > inverse sen and < inverse sen**2 : threshold = inverse_sensitivity
    # no. of point > inverse sen**2 : threshold = img_data.shape[0]//inverse_sensitivity
    #inverse_sensitivity = 20
    #if img_data.shape[0]//inverse_sensitivity > inverse_sensitivity:
    #    threshold = max(img_data.shape[0]//inverse_sensitivity, inverse_sensitivity)
    #else: 
    #    threshold = img_data.shape[0]
    threshold = getLogThreshold(img_data.shape[0], base=base, sensitivity=sensitivity)
    if img_data.shape[0]*255 - np.sum(img_data[:, x]) < threshold: # img_data.shape[0]//20 is arbitrary tolerance threshold, adaptive to how long is the line
        return True
    else:
        return False
    
def isLineWhiteH(img_data: np.array, y: int, base: float=20, sensitivity: float=100): 
    # no. of point < inverse sen : threshold = no. of point
    # no. of point > inverse sen and < inverse sen**2 : threshold = inverse_sensitivity
    # no. of point > inverse sen**2 : threshold = img_data.shape[1]//inverse_sensitivity
    #inverse_sensitivity = 20
    #if img_data.shape[1]//inverse_sensitivity > inverse_sensitivity:
    #    threshold = max(img_data.shape[1]//inverse_sensitivity, inverse_sensitivity)
    #else: 
    #    threshold = img_data.shape[1]
    threshold = getLogThreshold(img_data.shape[1], base=base, sensitivity=sensitivity)
    if img_data.shape[1]*255 - np.sum(img_data[y, :]) < threshold:  
        return True
    else:
        #print(img_data.shape[1]*255 - np.sum(img_data[y, :]), img_data.shape[1]//20)
        #print(y)
        return False    
    
def isPicWhite(img_data: np.array): # to avoid cutting words
    if img_data.shape[0]*img_data.shape[1]*255 - np.sum(img_data) < img_data.shape[0]*img_data.shape[1]:  # 10000 is arbitrary tolerance threshold
        return True
    else:
        return False

