# makepdf
**NOTE: Only intended for repo owner's personal use. Support is not planned at this moment.**
 - Script for compiling a batch of images to a pdf suitable for viewing on Kindle paperwhite (1024x768)
 - Can automatically trim a wide page / long page into multiple protrait pages

## Dependencies
 - python 3

to install dependencies:
```bash
pip install Pillow fpdf2
```

## How to use
- For cutting + compiling:\
clone the repo
```bash
python makepdf.py
```
input full directory containing the images you want to compile\
a PDF file will be generated

- Options available:\
bw: quantize image into black and white only\
sp: sharpen image\
for example:
```bash
python makepdf.py -sp
```


- For standalone use of horizontal cut for long image:\
clone the repo
```bash
python horizontalCut.py (into how many sections you want to break the image height: int, default=3)
```
for example
```bash
python horizontalCut.py 2
```
input full directory containing the images you want to edit\
a wide version of the long page will be generated for each page

