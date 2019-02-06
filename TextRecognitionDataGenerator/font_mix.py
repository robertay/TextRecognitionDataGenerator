# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import random
import os

class FontMix(object):

    @classmethod
    def randSpacing(self):
        return float(random.randint(-20,20))/10 # TODO fix hardcoded random spacing
    
    @classmethod
    def calcSpacing(self, spacing, font_size):
        return int((spacing - 1) * 2 * font_size / 70) 
        #return 1
    
    @classmethod
    def drawText(self, draw, x, y, string, font, spacing, fill, bounding_box):
        pixel_offset = spacing
        width_start = x
        char_rois = []
        vfill = fill
        for char in string:
            (w,h),(_,offset_y) = font.font.getsize(char) 
            vfill = max(0, fill + random.randint(-5,5)) # TODO fix hardcoded random character fill
            draw.text((width_start, y), char, fill=(vfill, vfill, vfill), font=font) 
            if bounding_box and char is not ' ':
                try:
                    base_x, base_y, top_x, top_y = font.getmask(char).getbbox()
                except:
                    print("Error with this font: ", font.getname(), " drawing this character: \'", char, "\', hex code: ", hex(ord(char.encode('utf-8'))))
                    raise
                char_rois.append((base_x + width_start, 
                                  base_y + y + offset_y, 
                                  top_x + width_start, 
                                  top_y + y + offset_y))
            width_start = width_start + w + pixel_offset
        return char_rois
    
    @classmethod
    def sizeText(self, font, string, spacing):
        pixel_offset = spacing
        total_width = 0
        total_height = 0
        for char in string:
            (w, h),(_, offset_y) = font.font.getsize(char)
            total_width += w + pixel_offset
            total_height = max(total_height, h + offset_y)    
        return (total_width, total_height)
    
    @classmethod
    def randSplit(self, word, splits):
        for splitLen in splits:
            if splitLen >= len(word):
                yield word
                break
            yield word[:splitLen]
            word = word[splitLen::]
    
    @classmethod
    def randGen(self, low,hi):
        while True:
            yield random.randint(low,hi)

    @classmethod                             
    def randomFont(self, fonts):
        font_file = fonts[random.randint(0, len(fonts) - 1)] 
        return font_file 
    
    class Text:
        def __init__(self, string, font_path, font_size):
            self.string = string
            self.font = ImageFont.truetype(font_path, size = random.randint(-20,20) + font_size) # TODO fix hardcoded random font size
            self.spacing = FontMix.calcSpacing(FontMix.randSpacing(), font_size)
            self.text_width, self.text_height = FontMix.sizeText(self.font, self.string, self.spacing) 
            self.ascent = self.font.font.ascent
    
    @classmethod
    def calcImageHeight(self, text_objects, image_ascent):
        adjusted_heights_list = []
        for text_object in text_objects:
            adjusted_heights_list.append(text_object.text_height + image_ascent - text_object.ascent)
        return max(adjusted_heights_list)
    
    @classmethod
    def drawImage(self, draw, text_objects, image_ascent, fill, bounding_box):
        width_start = 0
        string_rois = []
        for text_object in text_objects:
            string_rois += self.drawText(draw, width_start, image_ascent - text_object.ascent, text_object.string, text_object.font, text_object.spacing, fill, bounding_box)
            width_start += text_object.text_width
        return string_rois

    @classmethod
    def draw(self, text, fonts, fill, font_size, bounding_box):
        
        split_text = list(self.randSplit(text,self.randGen(1,len(text))))
        text_objects = []
        
        for string in split_text:
           text_objects.append(FontMix.Text(string, self.randomFont(fonts), font_size)) 
        
        image_width = sum(text_object.text_width for text_object in text_objects)
        image_ascent = max(text_object.ascent for text_object in text_objects)
        image_height = self.calcImageHeight(text_objects, image_ascent)
        
        text_image = Image.new('RGBA', (image_width + 5, image_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_image)
        string_rois = self.drawImage(draw, text_objects, image_ascent, fill, bounding_box)
        
        return text_image, string_rois
