import algorithum
from algorithum import ArrayQueue
from algorithum import ArrayStack
import math
import random
import numpy as np
import numpy.linalg as lin
from itertools import chain
import numpy.linalg as lin
import itertools
from algorithum import Node
#from Line import Lines
from enum import Enum
Drive = Enum('Drive','b c d')
class A:
    def __init__(self):
        self.index = 1
    def plus(self):
        self.index+=1
if __name__ == "__main__":
    d = np.array([[1, 4, 3],[6, 2, 4],[9, 3, 1]])
    y = np.array([[1] ,[2] ,[3],[4],[5],[6],[7],[8],[9]])

    a = np.random.randn(9, 2)
    print(a)
    print(y)
    b = np.dot(np.linalg.pinv(a),y)
    print(b)
    #t = np.array([[1,2],[2,3],[3,4]],[[1,2],[2,3]],[[1,2]])
    # print(ra)
    y = np.zeros((3,4,2))
    # for i in range(5-1):
    #     print(i)
    # print(math.fabs(np.array(-0.1)))
    # print(r.peek())
    # r = ArrayStack()
    # print(r.pop())
    # for i in range(-1,2):
    #     print(i)
    #s = np.array([1,2,3,4,5])
    #s = np.delete(s,2)
    #print(s)
    #s = np.append(s,[])
    #s[1][0] = 1
    #print(s)
    #for i in range(3):
    #    d[i][0] = x[i]**2
    #    d[i][1] = x[i]**1
    #if lin.det(d) == 0:
    #    print("fail")
    #else :
    #    result=np.dot(lin.inv(d),y)
        #print(result)
    #e = np.eye(2)
    #e.I
   #print(e)
   #for i in range(0,4):
   #    print(i)
    #    print(i)
        #X[i][0] = i**3
        #X[i][1] = i**2
        #X[i][2] = i**1
    # a = [[[0 for i in range()]]]
    # print(type(a))
    # a=np.array(a)
    # img = Origin_img
    # print(a)
    # list = [1,2,3,4]
    # for i in range(9):
    #     for j in range(i+1,10):
    #         print(i,j)
    # list = [0,0,0,0]
    # for i in range(len(list)) :
    #     list[i] = 0
    #
    # list =[[]]
    # print(len(list))
    # list[len(list)-1].append([0,0])
    # list.append([])
    # print(list)
    # print(len(list))
    # list[len(list)-1].append([0,0])
    #
    # print(list)
    # x = [0,0]
    # print(type(x[0]))
    # list = []
    # list.append([])
    # list[len(list)-1].append([0,0])
    # list[0].append([0,0])
    # list.append([])
    # list[len(list)-1].append([0,0])
    # list[1].append([0,0])
    # list[1].append([0, 0])
    # print(len(list[0]))
    # list = [[1 for col in range(20)]for row in range(10)]
    # print(len(list))
    # for i in range(len(list)) :