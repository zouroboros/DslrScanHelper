from math import sqrt

import numpy as np
import scipy.stats as stats

import dslr_scan_helper.lib as lib

def invert_and_stretch(context, img):
    if img.ndim == 2:
        return invert_bw(context, img)

    return invert_color(context, img)

def invert_bw(context, img):
    img = img.copy()

    histogram, _ = np.histogram(img, 2 ** 16, range = (0, 2**16 - 1))

    context.log_histogram("inverter", "bw histogram", histogram)

    min_value, max_value = find_interval(context, histogram)

    context.log_scalar("inverter", "min", min_value)
    context.log_scalar("inverter", "max", max_value)

    # re scaling of colors
    img = lib.rescale(img, max(0, min_value), min(2 ** 16 - 1, max_value), 0, 2**16 - 1)

    context.log_image("inverter", "streched image", img.copy())

    # inverting
    img = invert(context, img, 2 ** 16 - 1)

    return img.astype(np.uint16)

def invert_color(context, img):
    img = img.copy()

    # opencv works in bgr mode
    blue_histogram, _ = np.histogram(img[:, :, 0], bins = 2 ** 16, range = (0, 2**16 - 1))
    green_histogram, _ = np.histogram(img[:, :, 1], bins = 2 ** 16, range = (0, 2**16 - 1))
    red_histogram, _ = np.histogram(img[:, :, 2], bins = 2 ** 16, range = (0, 2**16 - 1))

    context.log_histogram("inverter", "blue", blue_histogram)
    context.log_histogram("inverter", "green", green_histogram)
    context.log_histogram("inverter", "red", red_histogram)

    blue_min, blue_max = find_interval(context, blue_histogram)
    green_min, green_max = find_interval(context, green_histogram)
    red_min, red_max = find_interval(context, red_histogram)

    context.log_scalar("inverter", "blue_min", blue_min)
    context.log_scalar("inverter", "blue_max", blue_max)
    context.log_scalar("inverter", "green_min", green_min)
    context.log_scalar("inverter", "green_max", green_max)
    context.log_scalar("inverter", "red_min", red_min)
    context.log_scalar("inverter", "red_max", red_max)

    # re scaling of colors
    img[:, :, 0] = lib.rescale(img[:, :, 0], max(0, blue_min), min(2 ** 16 - 1, blue_max), 0, 2**16 - 1)
    img[:, :, 1] = lib.rescale(img[:, :, 1], max(0, green_min), min(2 ** 16 - 1, green_max), 0, 2**16 - 1)
    img[:, :, 2] = lib.rescale(img[:, :, 2], max(0, red_min), min(2 ** 16 - 1, red_max), 0, 2**16 - 1)

    # inverting
    img[:, :, 0] = invert(context, img[:, :, 0], 2 ** 16 - 1)
    img[:, :, 1] = invert(context, img[:, :, 1], 2 ** 16 - 1)
    img[:, :, 2] = invert(context, img[:, :, 2], 2 ** 16 - 1)

    return img.astype(np.uint16)

def find_interval(context, histogram):
    dist = stats.rv_histogram((histogram, np.linspace(0, len(histogram), len(histogram) + 1)))
    return dist.interval(0.99)

def invert(context, img, max):
    img = img.copy()
    type = img.dtype
    img = max - img
    img[img < 0] = 0

    return img.astype(type)
