"""
Renders text from a CSV file to textures and applies them to multiple
objects.

Use snippets...

#at start of blender:

>>> import os, sys; sys.path.append(os.path.dirname(bpy.data.filepath)); import texture_painter

#on change:
>>> import importlib; importlib.reload(texture_painter); texture_painter.go()
"""

import codecs
import csv
import os

import bpy
from PIL import Image, ImageDraw, ImageFont

cwd = os.path.dirname(bpy.data.filepath)


def get_backers(csv_filename):
    with codecs.open(cwd + '\\' + csv_filename,
                     'r', 'utf-8-sig') as stream:
        iterable = csv.reader(stream)
        header = next(iterable)
        for row in iterable:
            backer = dict(zip(header, row))
            yield backer


def render_text_to_file(text_to_render, to_filename):
    # determine suitable image size
    pointsize = 50
    height = 64
    width = 512

    # create new PIL image with given size in RGB mode
    image = Image.new('RGB', (width, height))

    # load a suitable font
    font = ImageFont.truetype(font='arial.ttf', size=pointsize)

    # create new draw object from the image
    draw = ImageDraw.Draw(image)

    # rasterize the text into the draw object using the font
    draw.text(((height - pointsize) / 2,
               (height - pointsize) / 2),
              text_to_render, font=font, fill=(255, 255, 255, 255))

    # save image as test.png
    image.save(cwd + '\\texture_cache\\' + to_filename, 'PNG')


def read_csv():
    i = 0
    for backer in get_backers('backers_10.csv'):
        i += 1
        render_text_to_file(backer['Name'] + ', ' + backer['Country'],
                            format(i, "05d") + '.png')


def check_selection_rendermode():
    selected = bpy.context.selected_objects
    if len(selected) != 1:
        raise Exception("\n\nSelected objects: " + str(
            selected) + "; Must have exactly one prototype object selected")
    if (bpy.context.scene.render.engine != "BLENDER_RENDER"):
        raise Exception(
            '\n\nRendering mode is currently: ' + bpy.context.scene.render.engine + '; this script only works with Blender Render')


def go():
    print("Texture painter starting up.")
    check_selection_rendermode()
    # read_csv()
