import numpy as np

def rescale(array, old_min, old_max, new_min, new_max):
    result = array.astype(np.float32)
    result -= old_min

    result[result < 0] = 0

    result *= (new_max - new_min)
    result /= (old_max - old_min)
    result += new_min

    result[result > new_max] = new_max

    return result.astype(array.dtype)

def to8bit(img):
    return rescale(img, 0, 2**16, 0, 2**8).astype(np.uint8)
