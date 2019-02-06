import cv2
import numpy as np
import random
import math

from PIL import Image, ImageDraw

class ImageDegrader(object):
    @classmethod
    def gaussian_degrade(cls, input_image):
        """
            Degrade image with Gaussian noise 
        """
        image = np.array(input_image).astype(float)
        noise = np.copy(image).astype(float)

        cv2.randn(noise, 12, 4)

        output = np.clip(image - noise, 0, 255).astype("uint8")

        return Image.fromarray(output).convert('L')

    @classmethod
    def draw_line(cls, input_image, max_length, fill, width):
        """
            Draw a random line on the image
        """
        draw = ImageDraw.Draw(input_image)

        origin = (random.randint(0, input_image.size[0]), random.randint(0, input_image.size[1]))
        length_x = random.randint(-max_length, max_length)
        max_y = int(math.sqrt(max_length**2 - length_x**2))
        length_y = random.randint(-max_y, max_y)
        endpoint = np.add(origin, (length_x, length_y))

        draw.line((origin[0], origin[1], endpoint[0], endpoint[1]), fill = fill, width = width, joint = "curve")

