"""
Renders text from a CSV file to textures and applies them to multiple
objects.

Use snippets...

#at start of blender:

>>> import os, sys; sys.path.append(os.path.dirname(bpy.data.filepath)); import texture_painter

#on change:
>>> import importlib; importlib.reload(texture_painter); texture_painter.go()
"""

import bpy, os, sys
import codecs
import csv
import PIL
from PIL import Image, ImageDraw, ImageFont

def get_backers(csv_filename):
    with codecs.open(os.path.dirname(bpy.data.filepath) +
                             '\\' + csv_filename,
                     'r', 'utf-8-sig') as stream:
        iterable = csv.reader(stream)
        header = next(iterable)
        for row in iterable:
            backer = dict(zip(header, row))
            yield backer

def render_text_to_file(text_to_render):
    #determine suitable image size
    pointsize = 50
    height = pointsize*2
    width = pointsize*len(text_to_render) + 2*pointsize

    #create new PIL image with given size in RGB mode
    image = Image.new('RGB', (width,height))

    #load a suitable font
    font = ImageFont.truetype(font='arial.ttf', size=pointsize)

    # create new draw object from the image
    draw = ImageDraw.Draw(image)

    #rasterize the text into the draw object using the font
    draw.text((pointsize/2, pointsize/2),
              text_to_render, font=font, fill=(255,255, 255,255))

    #save image as test.png
    image.save(os.path.dirname(bpy.data.filepath) + '\\test.png', 'PNG')

def go():
    print("Texture painter starting up.")

    #Read through the CSV

    for backer in get_backers('backers_10.csv'):
        print(backer)
        render_text_to_file(backer['Name'])
        break

