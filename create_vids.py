import numpy as np

def simple(size = (64, 64)):
    """5 frames of solid color"""
    pixels = size[0] * size[1]
    ret = np.zeros((5, *size, 3))

    color = np.array([0x5E, 0xFC, 0x8D])
    ret[0, ...] = np.repeat(color, pixels).reshape((*size, 3))

    color = np.array([0x8E, 0xF9, 0xF3])
    ret[1, ...] = np.repeat(color, pixels).reshape((*size, 3))

    color = np.array([0x93, 0xBE, 0xDF])
    ret[2, ...] = np.repeat(color, pixels).reshape((*size, 3))

    color = np.array([0x83, 0x77, 0xD1])
    ret[3, ...] = np.repeat(color, pixels).reshape((*size, 3))

    color = np.array([0x6D, 0x5A, 0x72])
    ret[4, ...] = np.repeat(color, pixels).reshape((*size, 3))

    return ret

simple()