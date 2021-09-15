# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah
"""
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join

from utils import isLineWhiteV

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

def horizontalCut(img: Image):
    img_w, img_h = img.size
    bg_img = Image.new("L", (img_w*2, img_h//2), 255)
    bg_w_left = bg_img.size[0]
    
    
    return #img: rearranged image of dimension (w*2, h/2) of input image




if __name__ == '__main__':
    mypath = '.'
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-2:] != 'py']
    
    #for filename in filenames:
    #    load image
    #    horizontalCut(image)
    
    #    save image