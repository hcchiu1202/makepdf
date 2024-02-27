# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:59:21 2020

@author: justwah

script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite
"""

from PIL import Image
from fpdf import FPDF
import os
from os.path import isfile, join
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def addPDFPage(img: Image):
    pdf.add_page(orientation = 'P', format = (img.size[0], img.size[1])) 
    pdf.image(img, x=0, y=0, h=img.size[1]) #unit in mm


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
