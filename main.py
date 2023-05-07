import argparse
import sys
import PreProcessor as PreProcessor
from IO import IO
import Segmentation as Segmentation
from skimage.draw import rectangle_perimeter
from skimage import morphology
import numpy as np
from Classifier import Classifier


def main(input_folder, output_folder):
    io = IO()
    images, names = io.read_images(input_folder)
    io.output_folder = output_folder
    for image, name in zip(images, names):
        io.set_name(name)
        img = 1 - PreProcessor.to_binary_image(image)
        img, no_lines = PreProcessor.deskew_image(img, 6)
        staffs = Segmentation.segment_image(img, no_lines)
        io.write("{\n")
        for i in range(len(staffs)):
            classifier = Classifier()
            if staffs[i] is None:
                continue
            data = classifier.classify_staff(staffs[i])
            io.write("[" + data + "]")
            if i != len(staffs) - 1:
                io.write(",")
            io.write("\n")
        io.write("}")
        io.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input_folder", help="Input folder path")
    parser.add_argument("output_folder", help="Output folder path")
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder

    main(input_folder, output_folder)


def draw_rect(image, x1, x2, y1, y2, color, width):
    r, c = rectangle_perimeter((y1, x1), (y2, x2), shape=image.shape, clip=True)
    se = morphology.square(width)
    if color == 1:
        img = np.zeros(image.shape)
        img[r, c] = color
        img = morphology.dilation(img, se)
    else:
        img = np.ones(image.shape)
        img[r, c] = color
        img = morphology.erosion(img, se)

    if color == 1:
        image = np.logical_or(image, img)
    else:
        image = np.logical_and(image, img)

    return image
