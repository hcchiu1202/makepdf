# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 01:53:58 2021

@author: justwah
"""

import re
import imagesize
import numpy as np
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


def isLineWhiteV(img_data: np.array, x: int): # to avoid cutting words #maybe better count non-white point but more computation?
    reverse_sensitivity = 20
    if img_data.shape[0]//reverse_sensitivity > reverse_sensitivity:
        threshold = img_data.shape[0]//reverse_sensitivity 
    else: 
        threshold = img_data.shape[0]
    if (img_data.shape[0]*255 - np.sum(img_data[:, x])) < threshold: # img_data.shape[0]//20 is arbitrary tolerance threshold, adaptive to how long is the line
        return True
    else:
        return False
    
def isLineWhiteH(img_data: np.array, y: int): 
    reverse_sensitivity = 20
    if img_data.shape[1]//reverse_sensitivity > reverse_sensitivity:
        threshold = img_data.shape[1]//reverse_sensitivity 
    else: 
        threshold = img_data.shape[1]
    if (img_data.shape[1]*255 - np.sum(img_data[y, :])) < threshold:  
        return True
    else:
        #print(img_data.shape[1]*255 - np.sum(img_data[y, :]), img_data.shape[1]//20)
        #print(y)
        return False    
    
def isPicWhite(img_data: np.array): # to avoid cutting words
    if (img_data.shape[0]*img_data.shape[1]*255 - np.sum(img_data)) < (img_data.shape[0]*img_data.shape[1]):  # 10000 is arbitrary tolerance threshold
        return True
    else:
        return False

