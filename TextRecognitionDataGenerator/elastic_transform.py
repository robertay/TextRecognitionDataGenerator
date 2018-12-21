import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import cv2
from PIL import Image

class ElasticTransform(object):
    @classmethod
    def generate(cls, image, alpha_factor, sigma_factor, random_state=None):
	
        open_cv_image = np.array(image)
        alpha = open_cv_image.shape[1] * alpha_factor
        sigma = open_cv_image.shape[1] * sigma_factor

        if random_state is None:
            random_state = np.random.RandomState(None)

        shape = open_cv_image.shape
        	
        dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
        dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

        x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
        indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1))

        distorted_image = map_coordinates(open_cv_image, indices, order=1, mode='reflect')

        distorted_image = distorted_image.reshape(open_cv_image.shape)

        return Image.fromarray(distorted_image.astype('uint8'))
