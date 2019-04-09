# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import os


def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """

    if lang == 'cn':
        return [os.path.join('fonts/cn', font) for font in os.listdir('fonts/cn')]
    elif lang == 'ja':
        return [os.path.join('fonts/ja', font) for font in os.listdir('fonts/ja')]
    else:
        return [os.path.join('fonts/latin', font) for font in os.listdir('fonts/latin')]

for font_path in load_fonts(""):
    font = ImageFont.truetype(font_path)
    try:
        x1, y1, x2, y2 = font.getmask("¥").getbbox() 
    except:
        print(font.getname())
        pass
