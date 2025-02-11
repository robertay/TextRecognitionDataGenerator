import os
import random
import numpy as np

from PIL import Image, ImageFilter, ImageDraw

from computer_text_generator import ComputerTextGenerator
from elastic_transform import ElasticTransform
from roi_rotator import RoiRotator
try:
    from handwritten_text_generator import HandwrittenTextGenerator
except ImportError as e:
    print('Missing modules for handwritten text generation.')
from background_generator import BackgroundGenerator
from distorsion_generator import DistorsionGenerator

class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        return cls.generate(*t)

    @classmethod
    def draw_bounding_boxes(cls, image_dst, rois):
        drawbbox = ImageDraw.Draw(image_dst)
        for roi in rois:
            drawbbox.rectangle(roi, outline=0, fill=None) # Only works for grayscale images need outline=(0,0,0) for color

    @classmethod
    def generate(cls, index, text, fonts, out_dir, height, random_height, extension, skewing_angle, random_skew, 
                 blur, random_blur, background_type, random_bg, distorsion_type, distorsion_orientation, 
                 is_handwritten, name_format, width, random_width, alignment, bounding_box, view_bounding_box, random_alignment, text_color=-1):
        image = None

        #########################################################################
        # Randomly determine height between height and random_height variables  #
        #########################################################################
        if random_height > height: 
            height = random.randint(height, random_height)

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            image = HandwrittenTextGenerator.generate(text)
        else:
            image, rois = ComputerTextGenerator.generate(text, fonts, text_color, height, bounding_box)

        random_angle = random.randint(0-skewing_angle, skewing_angle)

        rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

        if bounding_box:
            rois = RoiRotator.compute(rois, random_angle, image.size, rotated_img.size) 


        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img # Mind = blown
        elif distorsion_type == 1:
            distorted_img = DistorsionGenerator.sin(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        elif distorsion_type == 2:
            distorted_img = DistorsionGenerator.cos(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        else:
            distorted_img = DistorsionGenerator.random(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )

        ##################################
        # Resize image to desired format #
        ##################################
        old_width = distorted_img.size[0]
        old_height = distorted_img.size[1]

        new_width = int(float(distorted_img.size[0]) * (float(height) / float(distorted_img.size[1])))
        
        resized_img = distorted_img.resize((new_width, height - 10), Image.ANTIALIAS)
        
        x_factor = new_width / old_width
        y_factor = (height - 10) / old_height 

        if bounding_box:
            i = 0
            for roi in rois:
                rois[i] = (np.array(roi) * np.array([x_factor, y_factor, x_factor, y_factor])).astype(int)
                i += 1

        if width > 0 and random_width > width:
            background_width = new_width + random.randint(width,random_width) 
        elif width > 0:
            background_width = width 
        else:
            background_width = new_width + 10 
        

        #############################
        # Generate background image #
        #############################
        if random_bg:
            background_type = random.randint(0,2)

        if background_type == 0:
            background = BackgroundGenerator.gaussian_noise(height, background_width)
        elif background_type == 1:
            background = BackgroundGenerator.plain_white(height, background_width)
        elif background_type == 2:
            background = BackgroundGenerator.quasicrystal(height, background_width)
        else:
            background = BackgroundGenerator.picture(height, background_width)


        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if random_alignment:
            alignment = random.randint(0,2)

        if alignment == 0:
            x_offset = 5
            background.paste(resized_img, (5, 5), resized_img)
        elif alignment == 1:
            x_offset = int(background_width / 2 - new_text_width / 2)
            background.paste(resized_img, (x_offset, 5), resized_img)
        else:
            x_offset = background_width - new_text_width - 5
            background.paste(resized_img, (x_offset, 5), resized_img)

        if bounding_box:
            i = 0
            for roi in rois:
                rois[i] = (np.array(roi) + np.array([x_offset, 5, x_offset, 5])).tolist()
                i += 1
        
        ##################################
        # Apply gaussian blur #
        ##################################

        blur_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else random.randint(0, blur))
            )
        )

        ##################################
        # Apply elastic transform #
        ##################################
        final_image = ElasticTransform.generate(blur_image, random.randint(0, 20) / 100 , random.randint(1, 100) / 100)

        #################################################
        # Apply width reduction to get skinny characters#
        #################################################
#        width_factor = random.randint(2,3)
#        
#        final_width = final_image.size[0]
#        final_height = final_image.size[1]
#        adjusted_width = int(final_width/width_factor)
#
#        final_image = final_image.resize((adjusted_width, final_height))
#
#        x_factor = adjusted_width / final_width
#        y_factor = 1 
#
#        i = 0
#        for roi in rois:
#            rois[i] = (np.array(roi) * np.array([x_factor, y_factor, x_factor, y_factor])).astype(int).tolist()
#            i += 1



        ##################################
        # Downsample to smaller image #
        ##################################
#        width, height = final_image.size
#        resize_factor = random.randint(20,30) / height 
#        final_image = final_image.resize((int(width * resize_factor), int(height * resize_factor)))
  
#        drawrois = ImageDraw.Draw(final_image)
#        for roi in rois:
#            drawrois.rectangle(roi, outline=0, fill=None)


        ##################################
        # Draw ROIs as a test #
        ##################################
        if bounding_box and view_bounding_box:
            FakeTextDataGenerator.draw_bounding_boxes(final_image, rois)

        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = '{}_{}.{}'.format(text, str(index), extension)
        elif name_format == 1:
            image_name = '{}_{}.{}'.format(str(index), text, extension)
        elif name_format == 2:
            image_name = '{}.{}'.format(str(index),extension)
        else:
            print('{} is not a valid name format. Using default.'.format(name_format))
            image_name = '{}_{}.{}'.format(text, str(index), extension)

        # Save the image
        final_image.convert('RGB').save(os.path.join(out_dir, image_name))
        return rois, index
