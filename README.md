# makepdf
 - Script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite (1024x768)
 - Can automatically trim a wide page into multiple protrait pages

# dependencies
pip install Pillow fpdf2

# How to use
- Download makepdf.py
- Place it in the directory containing images you want to compile
- run "python makepdf.py"

Only tested on Windows 10 command prompt

# TODO/issue
- make wrapper for standalone run .exe
- implement horizontal cut for long pages
- file size increase when handling wide pages, need investigate reason
