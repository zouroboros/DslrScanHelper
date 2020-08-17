from pathlib import Path
import subprocess
import itertools

import cv2 as cv

import dslr_scan_helper.auto_crop as auto_crop
import dslr_scan_helper.inverter as inverter

class DslrScanHelperApp:

    def __init__(self, context):
        self.context = context

    def convert(self, paths):
        paths = [Path(path) for path in paths]
        return itertools.chain([self.convert_file(path) for path in paths if path.is_file()],
            itertools.chain.from_iterable(self.convert_dir(path) for path in paths if path.is_dir()))

    def convert_file(self, path):
        output_path = path.with_suffix(".tiff")
        subprocess.run(["convert", "-depth", "16", path, output_path])
        return output_path

    def convert_dir(self, path):
        return [self.convert_file(file) for file in path.iterdir() if file.is_file()]

    def crop_file(self, file):
        img = cv.imread(f"{file}", cv.IMREAD_UNCHANGED)
        self.context.log_image("crop_file", "original", img)
        cropped_img = auto_crop.crop(self.context, img, auto_crop.find_corners_by_contours)
        new_file = f"{file.parent / file.stem}-cropped.tiff"
        cv.imwrite(new_file, cropped_img)
        return Path(new_file)

    def invert(self, file):
        img = cv.imread(f"{file}", cv.IMREAD_UNCHANGED)
        self.context.log_image("invert", "original", img)
        inverted_img = inverter.invert_color(self.context, img)
        new_file = f"{file.parent / file.stem}-inverted.tiff"
        cv.imwrite(new_file, inverted_img)
        return Path(new_file)

class DslrScanHelperContext:

    def log_scalar(self, context_name, name, value):
        return

    def log_image(self, context_name, name, img):
        return

    def log_histogram(self, context_name, name, histogram):
        return

    def end(self):
        return
