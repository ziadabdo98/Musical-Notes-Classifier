import numpy as np
from skimage.transform import resize
from skimage import img_as_bool
import Constants
import skimage as sk


class Note:
    def __init__(self, sy, ey, sx, ex, image):
        self.name = ""
        distance_to_y_up = self.__get_top_y(image)
        self.start_y = sy + distance_to_y_up
        distance_to_y_bottom = self.__get_bottom_y(image)
        self.end_y = sy + distance_to_y_bottom
        self.start_x = sx
        self.end_x = ex
        self.image = image[distance_to_y_up:distance_to_y_bottom]
        self.__set_image(self.image)
        self.normalized_image = img_as_bool(
            resize(self.image.astype(bool), Constants.NORMALIZED_IMAGE_SHAPE)
        )

    def __get_top_y(self, image):
        i = 0
        while np.any(image[i, :]) == False:
            i += 1
        return i

    def __get_bottom_y(self, image):
        i = image.shape[0] - 1
        while np.any(image[i, :]) == False:
            i -= 1
        return i

    def __get_left_x(self, image):
        i = 0
        while np.any(image[:, i]) == False:
            i += 1
        return i

    def __get_right_x(self, image):
        i = image.shape[1] - 1
        while np.any(image[:, i]) == False:
            i -= 1
        return i

    def __set_image(self, image):
        ratio = image.shape[0] / image.shape[1]
        if ratio < 2.05 and ratio > 1.95:
            self.image = self.__crop_image(image)

    def __crop_image(self, image):
        img = self.dopening(image, 7, 1)
        left_x = self.__get_left_x(img)
        right_x = self.__get_right_x(img)
        img = img[:, left_x:right_x]
        if abs(image.shape[1] - img.shape[1]) > img.shape[1] // 4:
            return img
        return image

    def dopening(self, image, width, height=1):
        se = sk.morphology.rectangle(width, height)
        img = sk.morphology.opening(image, se)
        return img
