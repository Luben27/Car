import cv2
import numpy as np
from Preparation import Preparation
from Line import Lines
import math
import ctypes
import string
# cam = cv2.VideoCapture(0)
# cam.set(3, 432)  # CV_CAP_PROP_FRAME_WIDTH
# cam.set(4, 240)  # CV_CAP_PROP_FRAME_HEIGHT
# cam.set(5,33) #CV_CAP_PROP_FPS
# // make kernel matrix for dilation and erosion (Use Numpy)
kernel_size_row = 3
kernel_size_col = 3
kernel = np.ones((3, 3), np.uint8)
value = True
index =46
lin = Lines()
def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image
if __name__ == "__main__":
    while index<=234:
        source = "rtsp://192.168.99.1/media/stream2"
        cap = cv2.VideoCapture(source)
        if cap.isOpened():
            cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, img = cap.read();
            cv2.imshow('demo', img)
            cv2.waitKey(10)

    cv2.destroyAllWindows()

