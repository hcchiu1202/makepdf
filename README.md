# makepdf
 - Script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite (1024x768)
 - Can automatically trim a wide page / long page into multiple protrait pages

# dependencies
 - python 3

 - to install dependencies: pip install Pillow fpdf2

# How to use
- Download makepdf.py
- Place it in the directory containing images you want to compile
- run "python makepdf.py"

Only tested on Windows 10 command prompt

# TODO/issue
- make wrapper for standalone run .exe (NOT DOING THIS since can easily do with pyinstaller, if file size is not a conern)
- DONE: implement horizontal cut for long pages
