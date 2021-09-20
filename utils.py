# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 01:53:58 2021

@author: justwah
"""

import re
import numpy as np
import math


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def getLogThreshold(dim: int, base: float=20, sensitivity: float=100):
    # larger base, threshold grow slower as img_data.shape increase (curve flatter)
    # larger sensitivity, looser detection
    threshold = math.log(dim, base) * sensitivity
    return threshold

def isLineWhiteV(img_data: np.array, x: int, base: float=20, sensitivity: float=100): # to avoid cutting words #maybe better count non-white point but more computation?
    threshold = getLogThreshold(img_data.shape[0], base=base, sensitivity=sensitivity)
    if img_data.shape[0]*255 - np.sum(img_data[:, x]) < threshold: # img_data.shape[0]//20 is arbitrary tolerance threshold, adaptive to how long is the line
        return True
    else:
        return False
    
def isLineWhiteH(img_data: np.array, y: int, base: float=20, sensitivity: float=100): 
    threshold = getLogThreshold(img_data.shape[1], base=base, sensitivity=sensitivity)
    if img_data.shape[1]*255 - np.sum(img_data[y, :]) < threshold:  
        return True
    else:
        return False    
    
def isPicWhite(img_data: np.array): # to avoid cutting words
    if img_data.shape[0]*img_data.shape[1]*255 - np.sum(img_data) < img_data.shape[0]*img_data.shape[1]: # arbitrary tolerance threshold
        return True
    else:
        return False

