#!/usr/bin/env python3

__author__ = 'Eqlion'

import sys

from PIL import Image
from os import path


PATH = path.join(path.dirname(__file__), '{}')


def save_(parts):
    for i, part in enumerate(parts):
        part.save(PATH.format('{}.jpg'.format(i)), 'JPEG')


def square_cut(img):
    w, h = img.size

    # Calculating how many pixels to cut from each of the sides
    spare = (w % h) // 2
    # Croping the image so that we could cut it into even parts
    img = img.crop((spare, 0, (w // h)*h + spare, h))
    w, h = img.size

    parts = [img.crop((h*i, 0, h*(i+1)-1, h)) for i in range(w // h)]
    save_(parts)

def square_fill(img):
    w, h = img.size

    # Creating `background` – an image with extra space on both sides
    background = Image.new('RGB', (w-(w%h)+h, h), 'white')
    # Calculating how many pixels to add to each of the sides
    spare = (background.size[0]-w) // 2

    background.paste(img, (spare, 0))
    w, h = background.size

    parts = [background.crop((h*i, 0, h*(i+1)-1, h)) for i in range(w // h)]
    save_(parts)

def poly_cut(img):
    w, h = img.size

    # Setting the ratio of the sides supported by Instagram
    neww = round(h * .8)
    # Calculating how many pixels to cut from each of the sides
    spare = (w % neww) // 2
    # Croping the image so that we could cut it into even parts
    img = img.crop((spare, 0, (w // h)*h + spare, h))
    w, h = img.size

    parts = [img.crop((neww*i, 0, neww*(i+1)-1, h)) for i in range(w // neww)]
    save_(parts)

def poly_fill(img):
    w, h = img.size

    # Setting the ratio of the sides supported by Instagram
    neww = round(h * .8)
    # Creating `background` – an image with extra space on both sides
    background = Image.new('RGB', (w-(w%neww)+neww, h), 'white')
    # Calculating how many pixels to add to each of the sides
    spare = (background.size[0]-w) // 2

    background.paste(img, (spare, 0))
    w, h = background.size

    parts = [background.crop((neww*i, 0, neww*(i+1)-1, h)) for i in range(w // neww)]
    save_(parts)

def auto(img):
    w, h = img.size
    d = {
      'square_cut(img)': (w % h) * h,
      'square_fill(img)': (h - (w % h)) * h,
      'poly_cut(img)': (w % round(h * .8)) * h,
      'poly_fill(img)': (round(h * .8) - (w % round(h * .8))) * h,
    }
    prefered = sorted(d, key=lambda x: d[x])[0]
    eval(prefered)

if __name__ == '__main__':
    img = Image.open(PATH.format(sys.argv[-1]))
    possible = {
      1: 'auto(img)',
      2: 'square_cut(img)',
      3: 'square_fill(img)',
      4: 'poly_cut(img)',
      5: 'poly_fill(img)',
    }
    print('Choose the way of cropping: \n')
    print('1. Auto (will select the best possible way)')
    print('2. Square (will create square images cutting off excess pixels from both sides)')
    print('3. Square (will create square images adding white stripes to both sides)')
    print('4. Rectangle (will create rectangle images cutting off excess pixels from both sides)')
    print('5. Rectangle (will create rectangle images adding white stripes to both sides)\n')
    print('Type (1-5): ')
    inp = int(input())
    while inp not in possible:
        print('Please enter a valid option.')
        inp = int(input())
    eval(possible[inp])
