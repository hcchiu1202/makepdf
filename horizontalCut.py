# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah
"""
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join

from utils import isLineWhiteV, isLineWhiteH, isPicWhite

'''
code for cutting and re-arranging pages with long text lay-out
TODO: make running standalone for image processing

pseudo: (for regular word page)
    load image
    make bg image < initialize available_width = bg_image.size[0]
    from y=100(or some threshold) scan upward for horizontal white line >> get UPPER
    scan from right to left for points of "vertical white line > non-white line" >> get list of v_cuts
        >between adjacent values in v_cuts should contain one column of word
    loop and crop(slice) image vertically according to v_cuts
        > (left, upper, right, lower) < (v_cuts[i+1], UPPER, v_cuts[i], img.size[1])
    for each slice:
        scan from middle point (slice.size[1]/2), downward, for horizontal whiteline >> avoid cutting a word in half
        paste upper part of slice (right=bg_image.available_width)
        bg_image.available_with -= slice.size[0]
        paste lower part of slice (right=bg_image.available_width)
        bg_image.available_with -= slice.size[0]
    return bg_image
    
TODO: handle exception page, e.g. with image-like chapter header etc
'''

def getHCuts(img:Image, 
            #upper:int, 
            #lower=None: int
            ):
    columns_bw = np.zeros((img.size[0]))
    img_data = np.asarray(img)
    for w in range(img.size[0]):
        if isLineWhiteV(img_data, w) == True:
            columns_bw[w] = 1
        else:
            columns_bw[w] = 0
    h_cuts = []
    for w in range(img.size[0] - 1):
        if columns_bw[w+1] - columns_bw[w] == 1:
            try:
                h_cuts.append(w+1+2)
            except IndexError:
                h_cuts.append(w+1)
    h_cuts.append(img.size[0])
    h_cuts.reverse()
    h_cuts.append(0)
    return h_cuts  


def horizontalCut(img: Image):
    y_scan = 100
    img_w, img_h = img.size
    bg_img = Image.new("L", (img_w*2, img_h//2), 255)
    bg_w_remain = bg_img.size[0]
    img_data = np.asarray(img)
    while isLineWhiteH(img_data, y_scan) == False:
        y_scan -= 1
    #print("passed first isLineWhite")
    h_cuts = getHCuts(img.crop((0, y_scan, img_w, img_h)))
    #print("hcuts:", h_cuts)
    for i in range(len(h_cuts) - 1):
        column = img.crop((h_cuts[i+1], y_scan, h_cuts[i], img_h))
        #print(column.size)
        h_scan = column.size[1] // 2
        column_data = np.asarray(column)
        #print(column_data.shape[0], h_scan)
        while isLineWhiteH(column_data, h_scan) == False:
            #print(h_scan)
            h_scan += 1
        #print("passed second isLineWhite")
        crop_ys = [0, h_scan, column.size[1]]
        for i in range(len(crop_ys) - 1):
            column_cropped = column.crop((0, crop_ys[i], column.size[0], crop_ys[i+1]))
            column_cropped_data = np.asarray(column_cropped)
            if isPicWhite(column_cropped_data) == True:
                continue
            bg_img.paste(column_cropped, (bg_w_remain - column.size[0], 0)) #tuple is (x, y) of top-left of the paste
            bg_w_remain -= column.size[0]
    return bg_img #img: rearranged image of dimension (w*2, h/2) of input image




if __name__ == '__main__':
    mypath = '.'
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-2:] != 'py']
    
    #for filename in filenames:
    #    load image
    #    horizontalCut(image)
    
    #    save image