#!/usr/bin/env python3

__author__ = 'Eqlion'

import sys

from PIL import Image
from os import path


PATH = path.join(path.dirname(__file__), '{}')

class Cropper(object):

    def __init__(self, img):
        self.img = img
        self.w, self.h = self.img.size

    def save_(self, parts):
        for i, part in enumerate(parts):
            part.save(PATH.format('{}.jpg'.format(i)), 'JPEG')

    def square_cut(self):
        # Calculating how many pixels to cut from each of the sides
        spare = (self.w % self.h) // 2
        # Croping the image so that we could cut it into even parts
        self.img = self.img.crop((spare, 0, (self.w // self.h)*self.h + spare, self.h))
        w, h = self.img.size

        parts = [self.img.crop((h*i, 0, h*(i+1)-1, h)) for i in range(w // h)]
        self.save_(parts)

    def square_fill(self):
        # Creating `background` – an image with extra space on both sides
        background = Image.new('RGB', (self.w-(self.w%self.h)+self.h, self.h), 'white')
        # Calculating how many pixels to add to each of the sides
        spare = (background.size[0]-self.w) // 2

        background.paste(self.img, (spare, 0))
        w, h = background.size

        parts = [background.crop((h*i, 0, h*(i+1)-1, h)) for i in range(w // h)]
        self.save_(parts)

    # def poly_cut(self):
    #     # Setting the ratio of the sides supported by Instagram
    #     neww = round(self.h * .8)
    #     # Calculating how many pixels to cut from each of the sides
    #     spare = (self.w % neww) // 2
    #     # Croping the image so that we could cut it into even parts
    #     self.img = self.img.crop((spare, 0, (self.w // self.h)*self.h + spare, self.h))
    #     w, h = self.img.size
    #
    #     parts = [self.img.crop((neww*i, 0, neww*(i+1)-1, h)) for i in range(w // neww)]
    #     self.save_(parts)
    #
    # def poly_fill(self):
    #     # Setting the ratio of the sides supported by Instagram
    #     neww = round(self.h * .8)
    #     # Creating `background` – an image with extra space on both sides
    #     background = Image.new('RGB', (self.w-(self.w%neww)+neww, self.h), 'white')
    #     # Calculating how many pixels to add to each of the sides
    #     spare = (background.size[0]-self.w) // 2
    #
    #     background.paste(self.img, (spare, 0))
    #     w, h = background.size
    #
    #     parts = [background.crop((neww*i, 0, neww*(i+1)-1, h)) for i in range(w // neww)]
    #     self.save_(parts)

    def auto(self):
        d = {
          'self.square_cut()': self.w % self.h,
          'self.square_fill()': self.h - (self.w % self.h),
          # 'self.poly_cut()': self.w % round(self.h * .8),
          # 'self.poly_fill()': round(self.h * .8) - (self.w % round(self.h * .8)),
        }
        prefered = sorted(d, key=lambda x: d[x])[0]
        eval(prefered)

if __name__ == '__main__':
    img = Image.open(PATH.format(sys.argv[-1]))
    cropper = Cropper(img)
    possible = {
      1: 'cropper.auto()',
      2: 'cropper.square_cut()',
      3: 'cropper.square_fill()',
      # 4: 'cropper.poly_cut()',
      # 5: 'cropper.poly_fill()',
    }
    print('\nChoose the way of cropping:')
    print('1. Auto (will select the best possible way)')
    print('2. Square (will create square images cutting off excess pixels from both sides)')
    print('3. Square (will create square images adding white stripes to both sides) \n')
    # print('4. Rectangle (will create rectangle images cutting off excess pixels from both sides)')
    # print('5. Rectangle (will create rectangle images adding white stripes to both sides)\n')
    print('Type (1-3): ')
    inp = int(input())
    while inp not in possible:
        print('Please enter a valid option.')
        inp = int(input())
    eval(possible[inp])
