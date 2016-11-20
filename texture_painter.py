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

def create_plaque(prototype, offset):
    prototype.select = True
    bpy.ops.object.duplicate_move(
        TRANSFORM_OT_translate={"value": offset})
    new_plaque = bpy.context.selected_objects[0]
    new_plaque.select = False
    return new_plaque

def get_offset(num, columns, spacing):
    """
    Return offset from prototype position.

    :param num: Number of plaques
    :param columns: Number of columns
    :param spacing: Spacing between plaques (x, y)
    :return: (x_offset, y_offset)
    """

    x_offset = (num % columns) * spacing[0]
    y_offset = (num // columns) * spacing[1]

    return (x_offset, y_offset)

def go():
    print("Texture painter starting up.")
    check_selection_rendermode()
    # read_csv()

    #pass in selected object
    prototype = bpy.context.selected_objects[0]
    create_plaque(prototype, (1, 0,0))
