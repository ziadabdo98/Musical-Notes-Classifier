# This class is responsible for pre-processing the image
import numpy as np
import skimage as sk
from skimage.transform import hough_line, hough_line_peaks, rotate
from Segmentation import hough_transform


def start(image):
    img = np.copy(image)
    img = to_binary_image(image)


def to_binary_image(image):
    img = np.copy(image)

    if img.ndim == 3:  # if image is rgb image
        if img.shape[2] == 4:  # if image contains alpha channel
            img = img[:, :, :3]
        img = sk.color.rgb2gray(img)

    img[img <= 0.5] = 0
    img = img.astype(bool).astype(float)
    return img


def deskew_image(image, angle_range):
    angle = get_image_angle(image, angle_range)

    no_lines = hough_transform(image, 6, 7)

    if abs(angle - 90) > 0.5:
        image = rotate(image.astype(float), angle - 90)
        no_lines = rotate(no_lines.astype(float), angle - 90)
        corrected = get_image_angle(image, angle_range)
    return image, no_lines


def get_image_angle(image, angle_range):
    angles = np.linspace(
        np.deg2rad(90 - angle_range), np.deg2rad(90 + angle_range), 360
    )
    h, theta, d = hough_line(image, angles)

    _, angles, _ = hough_line_peaks(
        h, theta, d, min_distance=9, min_angle=0, threshold=0.8 * np.amax(h)
    )
    return np.rad2deg(np.mean(angles))


def opening(image, width, height=1):
    se = sk.morphology.rectangle(width, height)
    img = sk.morphology.opening(image, se)
    return img


def closing(image, width, height):
    se = sk.morphology.rectangle(width, height)
    img = sk.morphology.closing(image, se)
    return img


def erosion(image, width, height):
    se = sk.morphology.rectangle(width, height)
    img = sk.morphology.erosion(image, se)
    return img


def sobel_v(img):
    v = sk.filters.sobel_v(img)
    v = v.astype(bool)
    return v
