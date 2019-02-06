import math
import random
import os
import numpy as np

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from font_mix import FontMix

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, fonts, text_color, font_size, bounding_box):

        txt_img, roi = FontMix.draw(text, fonts, text_color, font_size, bounding_box)

        
        return txt_img, roi
