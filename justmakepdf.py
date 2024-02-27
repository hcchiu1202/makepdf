# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah

script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite
"""

import numpy as np
from PIL import Image, ImageEnhance
from fpdf import FPDF
import os
from os.path import isfile, join
import argparse
import re

#from utils import sorted_alphanumeric, isLineWhiteV, isPicWhite
#from horizontalCut import horizontalCut


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

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

parser = argparse.ArgumentParser()
parser.add_argument('-hc', '--horizontal_cuts', type=int, default=3, help="rearrange image into 1/x of original height")
parser.add_argument('-sp', '--sharpen', action='store_true', help='sharpen the image')
parser.add_argument('-bw', '--blackwhite', action='store_true', help='quantize image into black and white only')
args = parser.parse_args()

mypath = input('Directory which contains image files:\n')
if mypath == '':
    mypath = os.getcwd()
filenames = sorted_alphanumeric(
    [f for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    )

device_w = 768
device_h = 1024
v_cut_threshold = 820
long_page_ratio = 0.6 #page w/h below this is long page

######################################

pdf = FPDF()

for filename in filenames:
    try:
        print(filename)
        img = Image.open(join(mypath, filename))
        addPDFPage(img)
        
    except Exception as e:
        print("unsupported file skipped: {} due to {}".format(filename, e))
        
print("Finished processing")

try:
    pdf.output(join(mypath, mypath[mypath.rfind('\\')+1:]+'.pdf'))
    print("OUTPUT: {}".format(join(mypath, mypath[mypath.rfind('\\')+1:]+'.pdf')))
except:
    pdf.output(join(mypath, 'output.pdf'))
    print("OUTPUT: {}".format(join(mypath, 'output.pdf')))
