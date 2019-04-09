import math
import random
import os
import numpy as np

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from font_mix import FontMix

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, fonts, fonts_ja, text_color, font_size, bounding_box):

#        jplist = ['〒', '年', '月', '日', '円']
#        if any(char in text for char in jplist):
#            fonts = fonts_ja
        txt_img, roi = FontMix.draw(text, fonts, fonts_ja, text_color, font_size, bounding_box)

        
        return txt_img, roi
