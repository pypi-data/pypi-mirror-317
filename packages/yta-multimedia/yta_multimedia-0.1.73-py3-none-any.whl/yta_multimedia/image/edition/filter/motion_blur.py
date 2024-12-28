"""
Thanks for the inspiration:
https://www.geeksforgeeks.org/opencv-motion-blur-in-python/
"""
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.image.converter import ImageConverter
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union

import cv2 
import numpy as np 


class MotionBlurDirection(Enum):
    """
    The direction we want to apply on the
    Motion Blur effect.
    """
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL_TOP_RIGHT = 'diagonal_top_right'
    DIAGONAL_TOP_LEFT = 'diagonal_top_left'

def apply_motion_blur(image: any, kernel_size: int = 30, direction: MotionBlurDirection = MotionBlurDirection.HORIZONTAL, output_filename: Union[str, None] = None):
    """
    Apply a motion blur effect on the given 'image'
    using the provided 'kernel_size' (the greater
    this value is, the more motion blur effect we
    will get on the image). The motion blur can be
    applied in one 'direction', and the result image
    can be stored locally if 'output_filename' is
    provided.
    """
    direction = MotionBlurDirection.to_enum(direction)

    # TODO: 'image' param type must be refactored
    image = ImageConverter.numpy_image_to_opencv(ImageParser.to_numpy(image))
    
    kernel = np.zeros((kernel_size, kernel_size)) 

    if direction == MotionBlurDirection.HORIZONTAL:
        kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size) 
    elif direction == MotionBlurDirection.VERTICAL:
        kernel[:, int((kernel_size - 1) / 2)] = np.ones(kernel_size) 
    elif direction == MotionBlurDirection.DIAGONAL_TOP_LEFT:
        np.fill_diagonal(kernel, 1)
    elif direction == MotionBlurDirection.DIAGONAL_TOP_RIGHT:
        np.fill_diagonal(np.fliplr(kernel), 1)
    
    # Normalize
    kernel /= kernel_size 
    
    # Apply the kernel
    image = cv2.filter2D(image, -1, kernel) 

    # TODO: Refactor this please
    if output_filename is not None:
        # Save output
        cv2.imwrite(f'a_a_car_mb_{str(kernel_size)}.jpg', image)

    image = ImageConverter.opencv_image_to_pillow(image)

    return image

