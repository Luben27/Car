import cv2
import numpy as np
from Preparation import Preparation
#from Line import Lines
from line_detect import Line
import math
kernel_size_row = 3
kernel_size_col = 3
kernel = np.ones((3, 3), np.uint8)
value = True
index = 0
lin = Line()
pre = Preparation()
if __name__ == "__main__":
    while index <= 1393:
        #print("index",index)
        img = cv2.imread("E:\\car\\imgOrigin%d.BMP" % index)  # 캠 이미지 불러오기
        cv2.imshow("img",img)
        HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        yellow = Preparation(HSV).Yellow_detect()
        erode=pre.erode(yellow)
        cv2.imshow("erode",erode)
        EDGE = pre.edge(erode)

        cv2.imshow("EDGE",EDGE)

        la = lin.labeling(EDGE, 10)
        cv2.imshow("label", la)
        ta = lin.ransac(EDGE,10,3)
        cv2.imshow("ransac", ta)



        #print(das)
        #cv2.imshow("das",das)
        #ea = np.array()
        #print(height,width)
        # pre.Green_mead(HSV, blue)
        # erode = cv2.erode(green, kernel, iterations=1)
        # green = pre.Green_detect(HSV)
        # erode = green.copy()
        # pre.erode(green,erode)
        # height, width = blue.shape[:2]
        # Erode = cv2.erode(blue, kernel, iterations=1)
        # # my = Preparation().erode(blue)
        #result = Preparation().find_mead_pixcel(erode)
        # print(pre.green_pixcel,pre.green_cnt)
        # if len(result)>1:
        #     if result[len(result)-1][1]<height*0.95:
        #         pre.Green_mead(HSV,erode)
        #         print(pre.green_cnt,pre.green_pixcel)
        # height, width = Erode.shape[:2]

        #lin.line_detect(result, origin)
        #
        # cv2.line(origin, (result[len(result)-1][0], result[len(result)-1][1]), (result[0][0], result[0][1]), (0, 0, 255), 3)

        # cv2.imshow("mead",Erode)
        # cv2.imshow("erode",erode)
        # cv2.imshow("green",green)
        # # cv2.imshow("green",erode)
        # cv2.imshow("hough", origin)
        # cv2.imshow("line",origin)
        # cv2.imshow("erode",erode)``
        #cv2.imshow("origin",origin)
        K = cv2.waitKey(0)
        # point = lin.mead_point
        # slope = lin.mead_slope
        # if len(point) >=2 and slope:
        #     if abs(slope) > 10:
        #         if point[1][0] > int(width * 0.6):
        #             print("roll 5")
        #             # self.mambo.fly_direct(roll=3, pitch=2, yaw=0, vertical_movement=0, duration=1)
        #         elif point[1][0] < int(width * 0.4):
        #             print("roll -5")
        #             # self.mambo.fly_direct(roll=-3, pitch=2, yaw=0, vertical_movement=0, duration=1)
        #         else:
        #             print("pitch 5")
        #             # self.mambo.fly_direct(roll=0, pitch=7, yaw=0, vertical_movement=0, duration=1)
        #     else:
        #         degree = int(math.atan2(1 / abs(slope), 1) * 180 / np.pi)
        #         if slope > 0:
        #             print("turn right", degree)
        #             # self.mambo.turn_degrees(degree)
        #         else:
        #             print("turn left", -degree)
        #             # self.mambo.turn_degrees(-degree)
        # self.mambo.turn_degrees(-degree)
        if K == 44:
            if (index > 0):
                index -= 1
        elif K == 46:
            if (index <= 1393):
                index += 1
        elif K == 27:
            index = 10000
        if K == 112:
            print("write!")
            # cv2.imwrite("test3.png", HSV)
