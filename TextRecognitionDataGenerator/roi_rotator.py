import numpy as np

class RoiRotator(object):

    @classmethod
    def compute(cls, rois, angle, image_size_before, image_size_after):
        rois_out = []
        image_center_before = RoiRotator.get_center(image_size_before)
        image_center_after = RoiRotator.get_center(image_size_after)

        for roi in rois:
            x1, y1 = RoiRotator.affine_transform(roi[0:2], angle, image_center_before, image_center_after)
            x3, y3 = RoiRotator.affine_transform(roi[2:4], angle, image_center_before, image_center_after)
            x4, y4 = RoiRotator.affine_transform((roi[0],roi[3]), angle, image_center_before, image_center_after)
            x2, y2 = RoiRotator.affine_transform((roi[2],roi[1]), angle, image_center_before, image_center_after)
            roi_out = RoiRotator.rectify(x1, x2, x3, x4, y1, y2, y3, y4)
            rois_out.append(roi_out)
        return rois_out 

    @classmethod
    def get_rotation_matrix(cls, angle):
        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        return np.matrix([[c, -s], [s, c]])

    @classmethod
    def affine_transform(cls, coordinates, angle, image_center_before, image_center_after):
        roi = np.asmatrix(coordinates)
        roi = roi - image_center_before
        roi = roi * RoiRotator.get_rotation_matrix(angle) + image_center_after
        return np.squeeze(np.asarray(roi)).astype(int)

    @classmethod
    def rectify(cls, x1, x2, x3, x4, y1, y2, y3, y4):
        x_topleft = x4 if x4 < x1 else x1
        y_topleft = y1 if y1 < y2 else y2
        x_bottomright = x2 if x2 > x3 else x3 
        y_bottomright = y3 if y3 > y4 else y4 

        return (x_topleft, y_topleft, x_bottomright, y_bottomright)
    
    @classmethod
    def get_center(cls, coordinates):
        return np.matrix([int(coordinates[0]/2), int(coordinates[1]/2)])
