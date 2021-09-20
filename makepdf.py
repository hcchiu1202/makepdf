# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah

script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite
"""
'''
pseudo:
    load
    if w > 768 and h > 1024:
        (cut white edge here?)
        resize
        (but how to determine resize according to which side?)
         - if w/h >0.65 resize to h=1024 
             - if after resize w < 820, go to 1 (just fit)
             - else go to 2 (wide page)
         - if w/h < 0.65 resize to w=768 (long page)
         
    1. regular page, no need cut
            
        > add to pdf
    2.  page need verticle cut (wide page)
        what criteria?
         > (loop) get v_cut point()
             make w//768 number of cut # this general to no matter how large is w

         >> adjustCutPoint (avoid cutting words)
         > get list of cut point (at least 1)
         > cut
         > get list of cutted image
         >> send to 1 and loop
         
         - elif w/h < 0.75 but h> xxxx (e.g. super long page)
    3. page need horizontal cut
        (to be implemented)
    4. irregular page <all no need preprocess

'''

import numpy as np
from PIL import Image
from fpdf import FPDF
import os
from os.path import isfile, join
#import tqdm
from utils import sorted_alphanumeric, isLineWhiteV, isPicWhite
from horizontalCut import horizontalCut



def verticalCut(img: Image):
    n_cut = img.size[0] // device_w
    segment_w = img.size[0] // (n_cut+1)
    v_cuts = [img.size[0]]
    v = img.size[0] - segment_w
    img_data = np.asarray(img)
    while v > 10:
        v_cache = v
        go_left = False
        while isLineWhiteV(img_data, v) == False:
            v += 1 # right shift the v_cut point until whole column is white
            if v == v_cuts[-1]:
                v = v_cache
                go_left = True                                                  # scan reverse direction
                break
            
        if go_left == True:
            while isLineWhiteV(img_data, v) == False:
                v -= 1
                if v == 0:
                    v_cuts.append(0)
                    return v_cuts

        v_cuts.append(v)
        go_left = False
        v -= segment_w
    v_cuts.append(0)
    return v_cuts #list of int of v_cut_point


def addPDFPage(img: Image):
    pdf.add_page(orientation = 'P', format = (img.size[0], img.size[1])) 
    pdf.image(img, x=0, y=0, h=img.size[1]) #unit in mm

def addWidePage(img: Image, v_cuts:list):
    for i in range(len(v_cuts)-1):
        cropped = img.crop((v_cuts[i+1], 0, v_cuts[i], img.size[1]))  #(left, upper, right, lower)
        cropped_data = np.asarray(cropped)
        if isPicWhite(cropped_data) == True:
            continue
        addPDFPage(cropped)

##### params #####
mypath = input('Directory which contains image files:\n')
if mypath == '':
    mypath = os.getcwd()
filenames = sorted_alphanumeric(
    [f for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    )

device_w = 768
device_h = 1024
v_cut_threshold = 820
long_page_ratio = 0.65 #page w/h below this is long page
page_mm_w = 270.9 #(270.9, 361.2)mm correspond to 768x1024 in 72dpi
page_mm_h = 361.2

######################################

pdf = FPDF()

for filename in filenames:
    try:
        print(filename)
        img = Image.open(join(mypath, filename))
        img = img.convert('L')
        img_w, img_h = img.size
        
        if img_w > device_w and img_h > device_h:                                           # if need resize
            if (img_w / img_h) > long_page_ratio:                                           # resize according to height (normal page, or wide page)
                img = img.resize((img_w*device_h//img_h, device_h), resample=Image.LANCZOS) # (width, height)
                if img.size[0] < v_cut_threshold:                                           # normal page
                    addPDFPage(img)
                else:                                                                       # wide page
                    v_cuts = verticalCut(img)
                    addWidePage(img, v_cuts)
            else:                                                                           # resize according to width (long page)
                img = img.resize((device_w, img_h*device_w//img_w), resample=Image.LANCZOS)
                img = horizontalCut(img)
                v_cuts = verticalCut(img)
                addWidePage(img, v_cuts)
                
        elif img_w < device_w and img_h < device_h:                                         # small page, direct add
            addPDFPage(img)
        else:                                                                               # strange ratio image
            if img_w <= device_w:
                addPDFPage(img)                                                                       # do nth at the moment, think later
            elif img_h <= device_h:
                addPDFPage(img)

    except:
        print("unsupported file skipped: {}".format(filename))
try:
    pdf.output(join(mypath, mypath[mypath.rfind('\\')+1:]+'.pdf'))
except:
    pdf.output(join(mypath, 'output.pdf'))

