import cv2
import numpy as np
import algorithum
import ctypes
# y-ax=b
class Preparation:
    def __init__(self, src=None):
        self.img=src
        self.green_cnt = 0
        self.green_pixcel = [0,0]
    #Color detect
    # def create_blank(width, height, rgb_color=(0, 0, 0)):
    #     """Create new image(numpy array) filled with certain color in RGB"""
    #     # Create black blank image
    #     image = np.zeros((height, width, 3), np.uint8)
    #
    #     # Since OpenCV uses BGR, convert the color first
    #     color = tuple(reversed(rgb_color))
    #     # Fill image with color
    #     image[:] = color
    #
    #     return image
    def Create_image(self,height,width,nchannels):
        if nchannels == 1:
            image = np.zeros((height,width),np.uint8)
        else :
            image = np.zeros((height,width,3),np.uint8)
        return image
    def Blue_detect(self):
        lower_blue = np.array([50, 50, 50])
        upper_blue = np.array([125, 255, 255])
        return cv2.inRange(self.img, lower_blue, upper_blue)
    def Blue_Erode_mead(self,src,dst):
        height, width = src.shape[:2]
        lower_blue = np.array([30, 40, 40])
        upper_blue = np.array([125, 255, 255])
        y = 0
        x = 0
        N = 0
        E = 0
        W = 0
        S = 0
        M = 0
        p1 = 0
        p2 = 0
        result = []
        for y in range(1,height-1):
            for x in range(1,width-1):
                M = (src[y][x][0]>=lower_blue[0] and src[y][x][0]<upper_blue[0] and src[y][x][1]>=lower_blue[1] and src[y][x][1]<upper_blue[1] and src[y][x][2]>=lower_blue[2] and src[y][x][2]<upper_blue[2])
                N = (src[y-1][x][0]>=lower_blue[0] and src[y-1][x][0]<upper_blue[0] and src[y-1][x][1]>=lower_blue[1] and src[y-1][x][1]<upper_blue[1] and src[y-1][x][2]>=lower_blue[2] and src[y-1][x][2]<upper_blue[2])
                S = (src[y+1][x][0]>=lower_blue[0] and src[y+1][x][0]<upper_blue[0] and src[y+1][x][1]>=lower_blue[1] and src[y+1][x][1]<upper_blue[1] and src[y+1][x][2]>=lower_blue[2] and src[y+1][x][2]<upper_blue[2])
                W = (src[y][x-1][0]>=lower_blue[0] and src[y][x-1][0]<upper_blue[0] and src[y][x-1][1]>=lower_blue[1] and src[y][x-1][1]<upper_blue[1] and src[y][x-1][2]>=lower_blue[2] and src[y][x-1][2]<upper_blue[2])
                E = (src[y][x+1][0]>=lower_blue[0] and src[y][x+1][0]<upper_blue[0] and src[y][x+1][1]>=lower_blue[1] and src[y][x+1][1]<upper_blue[1] and src[y][x+1][2]>=lower_blue[2] and src[y][x+1][2]<upper_blue[2])
                if M and N and S and W and E:
                    p1 = x
                    break
            x = width - 2
            while x >= 1:
                M = (src[y][x][0] >= lower_blue[0] and src[y][x][0] < upper_blue[0] and src[y][x][1] >= lower_blue[1] and src[y][x][1] < upper_blue[1] and src[y][x][2] >= lower_blue[2] and src[y][x][2] < upper_blue[2])
                N = (src[y - 1][x][0] >= lower_blue[0] and src[y - 1][x][0] < upper_blue[0] and src[y - 1][x][1] >=lower_blue[1] and src[y - 1][x][1] < upper_blue[1] and src[y - 1][x][2] >= lower_blue[2] and src[y - 1][x][2] < upper_blue[2])
                S = (src[y + 1][x][0] >= lower_blue[0] and src[y + 1][x][0] < upper_blue[0] and src[y + 1][x][1] >=lower_blue[1] and src[y + 1][x][1] < upper_blue[1] and src[y + 1][x][2] >= lower_blue[2] and src[y + 1][x][2] < upper_blue[2])
                W = (src[y][x - 1][0] >= lower_blue[0] and src[y][x - 1][0] < upper_blue[0] and src[y][x - 1][1] >=lower_blue[1] and src[y][x - 1][1] < upper_blue[1] and src[y][x - 1][2] >= lower_blue[2] and src[y][x - 1][2] < upper_blue[2])
                E = (src[y][x + 1][0] >= lower_blue[0] and src[y][x + 1][0] < upper_blue[0] and src[y][x + 1][1] >=lower_blue[1] and src[y][x + 1][1] < upper_blue[1] and src[y][x + 1][2] >= lower_blue[2] and src[y][x + 1][2] < upper_blue[2])
                if M and N and S and W and E:
                    p2 = x
                    break
                x -=1
            if (p1 != p2):
                result.append([int((p1+p2)/2),y])
                dst[y][int((p1+p2)/2)] = 100
        return result
    def erode(self,src):
        height, width = src.shape[:2]
        dst = src.copy()
        y = 0
        x = 0
        for y in range(1,height - 1):
            for x in range(1,width - 1):
                if src[y][x]&src[y-1][x]&src[y+1][x]&src[y][x+1]&src[y][x-1]:
                    dst[y][x] = 255
                else:
                    dst[y][x] = 0
        return dst
    def Green_mead(self,src,dst):
        height, width = src.shape[:2]
        cnt = 0
        self.green_cnt = 0
        self.green_pixcel = [0,0]
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([90, 255, 255])
        x = 0
        y = 0
        min_x = 400
        max_x = 0
        min_y = 400
        max_y = 0
        pixcel = [0,0,0]
        for y in range(1,height-1):
            for x in range(1,width -1):
                if src[y][x] and src[y+1][x] and src[y-1][x] and src[y][x+1] and src[y][x-1]:
                    if min_x>x:
                        min_x = x
                    if max_x<x:
                        max_x = x
                    if min_y>y:
                        min_y = y
                    if max_y<y:
                        max_y = y
                    self.green_cnt +=1
        if self.green_cnt>80:
            self.green_pixcel[0] = int((min_x + max_x) / 2)
            self.green_pixcel[1] = int((min_y + max_y) / 2)
            for y in range(self.green_pixcel[1]-1,self.green_pixcel[1]+1):
                for x in range(self.green_pixcel[0]-1,self.green_pixcel[0]+1):
                    dst[y][x] = 100
        else:
            self.green_cnt = 0
            self.green_pixcel = []
    def Green_detect(self,src):
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([90, 255, 255])
        return cv2.inRange(src,lower_green,upper_green)
    def Yellow_detect(self,img):
        lower_lig_green = np.array([15, 150, 50])
        upper_lig_green = np.array([30, 255, 255])
        return cv2.inRange(img, lower_lig_green, upper_lig_green)
    def labeling(self):
        stack=algorithum.ArrayStack()
        plant = self.img
    def edge(self,src):
        height, width = src.shape[:2]
        dst = src.copy()
        x = y = 0
        for x in range(0,width):
            dst[0][x] = 0
            dst[height-1][x] = 0
        for y in range(0,height):
            dst[y][0] = 0
            dst[y][width-1] = 0
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if src[y][x] != src[y + 1][x] or src[y][x] != src[y][x + 1]:
                    dst[y][x] = 255
                else:
                    dst[y][x] = 0
        return dst
    def im_trim(self,img): 
        height, width = img.shape[:2]
        x = int(0)
        y = int(height*0.4)  
        w = width-x
        h = int(height*0.8)  
        img_trim = img[y:h, x:w]  
        return img_trim 
    def find_edge_pixcel(self,img):
        height, width = img.shape[:2]
        result = []
        p1 = None
        p2 = None


    def find_mead_pixcel(self,img):
        height, width = img.shape[:2]
        result=[]
        p1 = None
        p2 = None
        for y in range(1,height-1):
            for x in range(1,width-1):
                if img[y][x] :
                    p1 = x
                    break
            x = width - 2
            while x >= 1 :
                if img[y][x] :
                    p2 = x
                    break
                x -= 1
            if not p1 == p2:
                if not (p1==0 and p2==width -2):
                    result.append([int((p1+p2)/2),y])
            p1 = 0
            p2 = 0
        return result
    def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  
        mask = np.zeros_like(img.img)  

        if len(img.img.shape) > 2:  
            color = color3
        else: 
            color = color1

        
        cv2.fillPoly(mask, vertices, color)

        
        ROI_image = cv2.bitwise_and(img, mask)

        return ROI_image
