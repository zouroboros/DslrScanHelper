import pytest
import numpy as np

from tests.test_context import TestContext
import dslr_scan_helper.inverter as inv

def test_invert_color():

        img = np.array([[[0, 0, 0], [64, 64, 64], [128, 128, 128], [192, 192, 192] , [255, 255, 255]]])

        inverted = inv.invert_color(TestContext(), img)

        assert np.array_equal(np.array([[[65535, 65535, 65535],
            [49155, 49155, 49155],
            [32768, 32768, 32768],
            [16381, 16381, 16381] ,
            [250, 250, 250]]]), inverted)
