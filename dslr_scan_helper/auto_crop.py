import cv2 as cv
import numpy as np
from math import sqrt

import dslr_scan_helper.lib as lib

def crop(context, img, corner_detector):
    gray = lib.to8bit(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
    gray = cv.blur(gray, (7, 7))
    gray = cv.equalizeHist(gray)
    context.log_image("auto_crop", "grayscale", gray.copy())
    _, binary = cv.threshold(gray, 200.0, 255, cv.THRESH_BINARY)
    context.log_image("auto_crop", "binary", binary.copy())
    corners = corner_detector(binary)
    _, corrected_img = correct_and_crop_rectangle(img, corners)
    return corrected_img


def find_corners_by_contours(binary_img):
    contours, _ = cv.findContours(cv.bitwise_not(binary_img), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    largestArea = 0

    for cnt in contours:
        area = cv.contourArea(cnt)

        if area > largestArea:
            largestArea = area
            largestContour = cnt
            points = cv.convexHull(cnt, returnPoints = True)

    points = list([x for [x] in points])

    height, width = binary_img.shape

    center = (width/2, height/2)
    center_x = width/2
    center_y = height/2

    top_left_points = [(x, y) for (x, y) in points if x < center_x and y < center_y]
    top_right_points = [(x, y) for (x, y) in points if x > center_x and y < center_y]
    bottom_left_points = [(x, y) for (x, y) in points if x < center_x and y > center_y]
    bottom_right_points = [(x, y) for (x, y) in points if x > center_x and y > center_y]

    top_left = max(top_left_points, key = lambda x: distance(center, x))
    top_right = max(top_right_points, key = lambda x: distance(center, x))
    bottom_left = max(bottom_left_points, key = lambda x: distance(center, x))
    bottom_right = max(bottom_right_points, key = lambda x: distance(center, x))

    return [top_left, top_right, bottom_left, bottom_right]

def correct_and_crop_rectangle(img, corners):
    [top_left, top_right, bottom_left, bottom_right] = corners
    width = int(min(distance(top_left, top_right), distance(bottom_left, bottom_right)))
    height = int(min(distance(top_left, bottom_left), distance(top_right, bottom_right)))

    new_top_left = (0, 0)
    new_top_right = (new_top_left[0] + width, new_top_left[1])
    new_bottom_left = (new_top_left[0], new_top_left[1] + height)
    new_bottom_right = (new_top_left[0] + width, new_top_left[1] + height)

    new_corners = [new_top_left, new_top_right, new_bottom_left, new_bottom_right]

    transformation = cv.getPerspectiveTransform(np.array(corners, np.float32), np.array(new_corners, np.float32))

    img_height, img_width, _ = img.shape

    return new_corners, cv.warpPerspective(img, transformation, (width, height))

def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2

    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
