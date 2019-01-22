import cv2
import numpy as np
import math
# -*- coding: cp949 -*-
# -*- coding: utf-8 -*-
class Lines:
    def __init__(self, Origin=None,mask=None):
       # self.x = np.array()
        self.Origin = Origin
        self.mask = mask
        self.mead_point = []
        self.mead_slope = None
    def erode(self,color):
        height, width = color.shape[:2]
    def line_detect(self,array,origin):
        height, width = origin.shape[:2]
        length = len(array)
        i = 0
        max_cnt = 0
        max_line = []
        cnt = 0
        a = None
        b = None
        for n in range(10,height):
            while (i+n) < length:
                cnt = 0
                F=array[i]
                L=array[i+n]
                if F[0]==L[0]:
                    for i in range(length):
                        if abs(array[i][0]-F[0])<2:
                            a = 1000
                            b = F[0]
                            cnt += 1
                elif F[1]==L[1]:
                    for i in range(length):
                        if abs(array[i][1]-F[1])<2:
                            a = 0
                            b = F[1]
                            cnt += 1
                else :
                    a = (F[1] - L[1])/(F[0] - L[0])
                    b = F[1] - a*F[0]
                    for j in range(length):
                        x = (array[j][1] - b)/a
                        if abs(array[j][0]-x)<2:
                            cnt+=1
                if max_cnt <= cnt:
                    max_cnt = cnt
                    max_line = [a,b]
                i+=3
        if len(max_line)==2:
            a = max_line[0] 
            b = max_line[1] 
            if a == 1000:   
                b = int(b)
                F = [[b,height-1],[b,0]]
                # x = [b,b]
                # y = [0,height-1]
            elif a == 0:                
                b = int(b)
                F = [[0,b],[width-1,b]]
                # x = [0,width-1]
                # y = [b,b]
            else :
                F = []                  
                i = width - 1           
                cnt = int(a*i + b)      
                if cnt>=0 and cnt<height:
                    F.append([i,cnt])
                i = 0
                cnt = int(b)
                if cnt>=0 and cnt<height:
                    F.append([i, cnt])
                i = height - 1
                cnt = int((i-b)/a)
                if cnt>=0 and cnt<width: 
                    F.append([cnt, i])
                i = 0
                cnt = int(-b/a)
                if cnt>=0 and cnt<width: 
                    F.append([cnt, i])
                if F[0][1]>F[0][0]:
                    i = F[0]             
                    F[0] = F[1]
                    F[1] = i
             

            self.mead_point = F
            self.mead_slope = a
            cv2.line(origin, (F[0][0], F[0][1]), (F[1][0], F[1][1]), (0,0,255), 3)
        else :
            self.mead_point = []
            self.mead_slope = None
            return origin
