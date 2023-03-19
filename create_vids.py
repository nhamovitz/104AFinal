import numpy as np
import cv2

def simple(size = (64, 64)):
    """5 frames of solid color"""
    pixels = size[0] * size[1]
    ret = np.zeros((5, *size, 3), dtype=np.uint8)

    color = np.array([0x8D, 0xFC, 0x5E])
    ret[0, ...] = np.tile(color, pixels).reshape((*size, 3))

    color = np.array([0xf3, 0xF9, 0x8e])
    ret[1, ...] = np.tile(color, pixels).reshape((*size, 3))

    color = np.array([0xdf, 0xBE, 0x93])
    ret[2, ...] = np.tile(color, pixels).reshape((*size, 3))

    color = np.array([0xd1, 0x77, 0x83])
    ret[3, ...] = np.tile(color, pixels).reshape((*size, 3))

    color = np.array([0x72, 0x5A, 0x6d])
    ret[4, ...] = np.tile(color, pixels).reshape((*size, 3))

    return ret

def color_wheel():
    pass




def sun():
    """5x3 with movement"""

    light_blue = [240, 200, 35]
    yellow = [60, 248, 250]
    green = [29, 135, 34]

    frames = np.array(
        [
         [
          [light_blue]*5,
          [yellow, light_blue,light_blue,light_blue, yellow,],
          [green] * 5
         ],
         [
          [light_blue, yellow, light_blue, light_blue, light_blue],
          [light_blue]*5,
          [green] * 5
         ],
         [
          [light_blue, light_blue, yellow, light_blue, light_blue],
          [light_blue]*5,
          [green] * 5
         ],
         [
          [light_blue, light_blue, light_blue, yellow, light_blue],
          [light_blue]*5,
          [green] * 5
         ],
         [
          [light_blue]*5,
          [light_blue, light_blue, light_blue, light_blue, yellow],
          [green] * 5
         ],
        ], dtype = np.uint8
    )
   
    # light_blue = np.tile(light_blue, 100**2).reshape((100, 100, 3))
    # yellow = np.tile(yellow, 100**2).reshape((100, 100, 3))
    # green = np.tile(green, 100**2).reshape((100, 100, 3))

    row_shape = (5, 100, 500, 3)
    frames = np.zeros((5, 300, 500, 3), dtype = np.uint8)
    frames[:, 0:100, :, :] = np.broadcast_to(light_blue, row_shape)
    frames[:, 100:200, :, :] = np.broadcast_to(light_blue, row_shape)
    frames[:, 200:300, :, :] = np.broadcast_to(green, row_shape)

    frames[0, 100:200, 0:100, :] = np.broadcast_to(yellow, (1, 100, 100, 3))
    frames[1, 0:100, 100:200, :] = np.broadcast_to(yellow, (1, 100, 100, 3))
    frames[2, 0:100, 200:300, :] = np.broadcast_to(yellow, (1, 100, 100, 3))
    frames[3, 0:100, 300:400, :] = np.broadcast_to(yellow, (1, 100, 100, 3))
    frames[4, 100:200, 400:500, :] = np.broadcast_to(yellow, (1, 100, 100, 3))
    
    # assert frames.shape == ((5, 3, 5, 3))
    return frames

if __name__ == '__main__':
    # turns out opencv reads each pixel as
    # b, g, r

    red = np.array([255, 0, 0], dtype=np.uint8)
    red = np.tile(red, 400**2).reshape((400, 400, 3))
    while True:
        cv2.imshow("red", red)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break