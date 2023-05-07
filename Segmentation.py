from skimage.transform import hough_line, hough_line_peaks
import numpy as np
from Staff import Staff
import PreProcessor
from StaffLine import StaffLine


def segment_image(image, no_lines):
    image_with_lines = get_lines_image(image)
    staff_lines = get_staff_lines(image_with_lines)
    if len(staff_lines) % 5 == 0:
        staffs = get_staffs(staff_lines, no_lines)
        return staffs
    else:
        return []


def hough_transform(img, angle_range, width):
    angles = np.linspace(
        np.deg2rad(90 - angle_range), np.deg2rad(90 + angle_range), 360
    )
    h, theta, d = hough_line(img, angles)

    image = np.copy(img)
    origin = np.array((0, img.shape[1]))
    for _, angle, dist in zip(
        *hough_line_peaks(
            h, theta, d, min_distance=9, min_angle=0, threshold=0.8 * np.amax(h)
        )
    ):
        y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
        section = image[min(int(y0), int(y1)) - 5 : max(int(y0), int(y1)) + 5, :]
        image[
            min(int(y0), int(y1)) - 5 : max(int(y0), int(y1)) + 5, :
        ] = PreProcessor.opening(section, width)
    return image


def get_lines_image(image):
    lines = np.zeros(image.shape)
    for i in range(2, 10):
        lines += image - PreProcessor.opening(image, i, 1)
    return lines.astype(bool)


def get_staff_lines(image):
    staff_lines = []
    max_count = 0
    for i in range(image.shape[0] - 1):
        row = image[i, :]
        if any(row):
            count = sum(row)
            if count > max_count:
                max_count = count
            staff_lines.append(StaffLine(i, row))
    staff_lines = remove_empty_lines(staff_lines, max_count)
    staff_lines = collect_lines(staff_lines)
    return staff_lines


def remove_empty_lines(staff_lines, max_count):
    half = max_count // 2
    lines = []
    for line in staff_lines:
        if line.count > half:
            lines.append(line)
    return lines


def collect_lines(lines):
    list_of_lines = []
    list_of_list = []
    list_of_lines.append(lines[0])
    for i in range(1, len(lines)):
        if abs(lines[i - 1].y - lines[i].y) > 6:
            list_of_list.append(list_of_lines)
            list_of_lines = []
            list_of_lines.append(lines[i])
        else:
            list_of_lines.append(lines[i])
    list_of_list.append(list_of_lines)
    count = 0
    final_lines = []
    sxs = []
    exs = []
    for lst in list_of_list:
        y = []
        for line in lst:
            y.append(line.y)
            sxs.append(line.start_x)
            exs.append(line.end_x)
        count += 1
        lst[0].y = int(np.mean(y))
        final_lines.append(lst[0])

    for line in final_lines:
        line.start_x = int(np.median(sxs))
        line.end_x = int(np.median(exs))
    return final_lines


def get_staffs(lines, image):
    staffs = []
    for i in range(0, len(lines), 5):
        sy = lines[i].y
        ey = lines[i + 4].y
        sx = lines[i].start_x
        ex = lines[i].end_x
        staff_height = ey - sy
        ymin = max(sy - staff_height / 2, 0)
        ymax = min(ey + staff_height / 2, image.shape[0] - 1)
        while np.any(image[sy, :]) and sy > ymin:
            sy -= 1
        while np.any(image[ey, :]) and ey < ymax:
            ey += 1
        image_cpy = image[sy:ey, sx:ex]
        staff = Staff(sy, ey, sx, ex, image_cpy, lines[i : i + 5])

        staffs.append(staff)
    return staffs
