import numpy as np
from matplotlib import pyplot as plt

from dslr_scan_helper.app import DslrScanHelperContext
import dslr_scan_helper.lib as lib

class DebugContext(DslrScanHelperContext):

    def log_scalar(self, context_name, name, value):
        print(f"{context_name}: {name}={value}")

    def log_image(self, context_name, name, img):
        plt.figure(f"{context_name}: {name}")
        if img.dtype == np.uint16:
            img = lib.to8bit(img)

        if img.ndim == 2:
            plt.imshow(img, cmap='gray')
        elif img.ndim == 3:
            plt.imshow(img)

    def log_histogram(self, context_name, name, histogram):
        plt.figure(f"{context_name}: {name}")
        plt.bar(x = np.linspace(0, len(histogram) - 1, num=len(histogram)), height=histogram)

    def end(self):
        plt.show()
