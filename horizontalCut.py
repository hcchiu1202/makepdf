# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah
"""
import numpy as np
from PIL import Image
import sys
import os
from os.path import isfile, join

from utils import sorted_alphanumeric, isLineWhiteV, isLineWhiteH, isPicWhite



def getHCuts(img:Image):
    columns_bw = np.zeros((img.size[0]))
    img_data = np.asarray(img)
    for w in range(img.size[0]):
        if isLineWhiteV(img_data, w, sensitivity=70) == True:
            columns_bw[w] = 1
        else:
            columns_bw[w] = 0
    h_cuts = []
    for w in range(img.size[0] - 1):
        if columns_bw[w+1] - columns_bw[w] == 1:
            try:
                h_cuts.append(w+1+2)
                column_margin = True
            except IndexError:
                h_cuts.append(w+1)
                column_margin = False
    if len(h_cuts) == 1: #if page only have one line of text
        if column_margin == True:
            v = h_cuts[0]-1-2
        else:
            v = h_cuts[0]-1
        while isLineWhiteV(img_data, v) == False:
            v -= 1
        h_cuts.insert(0, v)
    h_intervals = []
    for i in range(len(h_cuts) - 1):
        h_intervals.append(h_cuts[i+1] - h_cuts[i])
        h_interval_mean = int(sum(h_intervals) / (len(h_cuts) - 1))
    
    h_cuts.append(img.size[0])
    h_cuts.reverse()
    if h_cuts[-1] > h_interval_mean:
        h_cuts.append(h_cuts[-1] - h_interval_mean)
    h_cuts.append(0)
    return h_cuts  


def horizontalCut(img: Image, split: int = 3):
    y_scan = 100
    img_w, img_h = img.size
    bg_img = Image.new("L", (img_w*split, img_h//split), 255)
    bg_w_remain = bg_img.size[0]
    img_data = np.asarray(img)
    while isLineWhiteH(img_data, y_scan, sensitivity=80) == False:
        y_scan -= 1
    h_cuts = getHCuts(img.crop((0, y_scan, img_w, img_h)))
    for i in range(len(h_cuts) - 1):
        column = img.crop((h_cuts[i+1], y_scan, h_cuts[i], img_h))
        crop_ys = []
        for i in range(split - 1):
            h_scan = (column.size[1] // split) * (i+1)
            column_data = np.asarray(column)
            while isLineWhiteH(column_data, h_scan) == False:
                h_scan += 1
            if len(crop_ys) > 0 and h_scan == crop_ys[-1]:
                continue
            crop_ys.append(h_scan)
        crop_ys.insert(0, 0)
        crop_ys.append(column.size[1])
        
        for i in range(len(crop_ys) - 1):
            column_cropped = column.crop((0, crop_ys[i], column.size[0], crop_ys[i+1]))
            column_cropped_data = np.asarray(column_cropped)
            if isPicWhite(column_cropped_data) == True:
                continue
            bg_img.paste(column_cropped, (bg_w_remain - column.size[0], 0)) #tuple is (x, y) of top-left of the paste
            bg_w_remain -= column.size[0]
            
    bg_img_data = np.asarray(bg_img)                # trim white area unused in bg
    v = 0
    while isLineWhiteV(bg_img_data, v) == True:
        v += 1                                      # right shift the v_cut point until whole column is white
    bg_img = bg_img.crop((max(0, v - 10), 0, bg_img.size[0], bg_img.size[1]))
    return bg_img #img: rearranged image of dimension (w*2, h/2) of input image - the trimmed white area at left side




if __name__ == '__main__':
    if len(sys.argv) == 2:
        split = int(sys.argv[1])
    mypath = input('Directory which contains image files:\n')
    if mypath == '':
        mypath = os.getcwd()
    filenames = sorted_alphanumeric(
        [f for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        )
    
    for filename in filenames:
        print(filename)
        pth = join(mypath, filename)
        img = Image.open(pth)
        img = img.convert('L')
        try:
            img = horizontalCut(img, split)
        except:
            img = horizontalCut(img)
        
        img.save(pth[:pth.rfind(".")] + "_w" + pth[pth.rfind("."):])
        
    print("Finished processing horizontal cutting")
        
