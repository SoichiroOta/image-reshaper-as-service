import io

import cv2
import numpy as np
from PIL import Image


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def load_img(bytes_io):
    return pil2cv(Image.open(bytes_io).convert('RGB'))


def save_img(cv_image, format_str='PNG'):
    with io.BytesIO() as bytes_io:
        cv2pil(cv_image).save(bytes_io, format=format_str)
        return bytes_io.getvalue()


def reshape(cv_img, size):
    height, width, _ = cv_img.shape

    side = min(height, width)

    hside = int(side / 2)
    hheight = int(height/2)
    hwidth = int(width/2)
    center_img = cv_img[
        hheight - hside:hheight + hside, hwidth - hside:hwidth+hside
    ]

    return cv2.resize(center_img, (size, size))
