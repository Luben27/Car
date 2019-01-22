# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
import random
from Preparation import Preparation as pre
from algorithum import ArrayStack as Stack
import numpy as np
import numpy.linalg as lin

class Line:
	def __init__(self):
		self.d = np.array([[0, 0, 1],[0, 0, 1],[0, 0, 1]])
		self.labe_arr = np.array([])    
		self.labe_cnt = np.array([])    
		self.start_point = np.array([])
		self.last_point = np.array([])
		self.label = 0
		self.tmp = np.array([])
	def inital(self,height,width):
		self.tmp = pre().Create_image(height,width,1) 
		self.height = height
		self.width = width 
	def ransac(self,src,n,thres):
		if self.label == 0:
			return src
		height, width = src.shape[:2]
		result = np.zeros((self.label,3))
		sample = np.zeros((1,3))
		rand_array = np.zeros((3,2))
		arr_index = np.zeros(3)
		loop = 0
		cnt = 0
		Max_cnt = 0
		Max_index = 0
		T = thres
		for L in range(self.label):
			loop = 0
			Max_cnt = 0
			while loop < n:
				cnt = 0
			   
				i = 0
				while i<3:
					rand_index = int(np.random.choice(self.labe_cnt.item(L),1))
					j = 0
					while j < i:
						if arr_index.item(j) == rand_index:
					    		break
						j += 1
					if j != i :
						continue
					arr_index.itemset(i,rand_index)
					rand_array.itemset(i,0,self.labe_arr.item(L,rand_index,0))
					rand_array.itemset(i,1,self.labe_arr.item(L,rand_index,1))
					i += 1


				#print(rand_array)
				for i in range(3):
					self.d.itemset(i,0, (rand_array.item(i,0) ** 2))
					self.d.itemset(i,1,rand_array.item(i,0))
				if lin.det(self.d) == 0:
					continue
				else:
				    	y = rand_array[:, 1]
				    	sample = np.dot(lin.inv(self.d), y)
				#print(rand_array)
				x = self.start_point.item(L,0)
				for i in range(self.labe_cnt.item(L)): 
					y = np.dot(np.array([x*x,x,1]),sample)        
					residual = math.fabs(self.labe_arr.item(L,i,1) - y)        
					#print(self.labe_arr[L][i] , x,y)
					if residual <= T:
					    	cnt += 1
					x += 1
				if Max_cnt < cnt:
					result[L] = sample
					Max_cnt = cnt
				loop += 1
		    	A2 = np.zeros((Max_cnt,3),np.float32)
		    	B2 = np.zeros((Max_cnt,1),np.float32)
		    	x = self.start_point.item(L,0)
		    	cnt = 0
		    	for i in range(self.labe_cnt.item(L)): 
		        	y = np.dot([x * x, x, 1], result[L])  
		        	residual = math.fabs(self.labe_arr.item(L,i,1) - y)  
		        	# print(self.labe_arr[L][i] , x,y)
		        	if residual <= T:
		            		A2[cnt] = [x*x, x, 1]
		            		B2[cnt] = np.float32(self.labe_arr.item(L,i,1))
		            		cnt += 1
		        	x += 1
		    	Row,Col = lin.pinv(A2).shape[:2]
		    	Row, Col = B2.shape[:2]
		    	result[L] = np.dot(lin.pinv(A2), B2).T[0]
		    
		#return self.drow_grape(src=src,point = result)
	def drow_grape(self,src,point):
		row = int(self.label)
		height, width = src.shape[:2]
		dst = pre().Create_image(height, width, 1)
		result = 0.0
		a = b = c = 0.0
		color = 255 / row
		dis = 0
        
		for i in range(row):
		    	a = point[i][0]
		    	b = point[i][1]
		    	c = point[i][2]
		    	first_x = self.start_point[i][0]
		    	last_x = self.last_point[i][0]
		    	if self.last_point[i][1] > self.start_point[i][1]:
		        	first_y = self.start_point[i][1]
		        	last_y = self.last_point[i][1]
		    	else :
		        	last_y = self.start_point[i][1]
		        	first_y = self.last_point[i][1]
		    	first_x = self.labe_arr[i][0][0]
		    	last_x = self.labe_arr[i][self.labe_cnt[i]-1][0]
		    	print(i,first_x, last_x)
		    	#print(self.labe_arr[i])
		    	first_y = 0
		    	last_y = height - 1
		    	for x in range(first_x,last_x + 1):
		        	result = a * x * x + b * x + c
		        	if result >= first_y and result <= last_y:
		            		dst[int(result)][x] = color * (i + 1)
		    	for y in range(first_y,last_y + 1):
		        	dis = (b *b - 4*(a * (c - y)))
		        	if a != 0:
		            		if dis > 0 :
		                		dis = math.sqrt(dis)
		                		x = (-b + dis) / (2 * a)
		                		if x >=first_x and x < last_x:
		                    			dst[y][int(x)] = color * (i + 1)
		                		x = (-b - dis) / (2 * a)
		                		if x >= first_x and x < last_x:
		                    			dst[y][int(x)] = color * (i + 1)
		            		elif dis == 0:
		                		x = (-b)/(2*a)
		                		if x >= first_x and x < last_x:
		                    			dst[y][int(x)] = color * (i + 1)
		        	else :
		            		if b != 0:
		                		x = (y-c)/b
		                		if x >= first_x and x < last_x:
		                    			dst[y][int(x)] = color * (i + 1)
		return dst

	def labeling(self,src,thres): 
		height, width = src.shape[:2]
		#labeling
		numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(src, connectivity=8)
		hash_cnt = 0    
		#hash
		hash = np.zeros(numOfLabels, np.int32)
		index_list = list()
		print hash
		max_L = 0
		L = 0
		for i in range(1,numOfLabels):
			if stats[i][4] > thres :
				hash_cnt += 1
				hash[i] = hash_cnt
				index_list.append(i)
				L = stats[i][2] + 1
				if max_L < L:
					max_L = L
		output = np.zeros(src.shape, np.uint8)
		if hash_cnt != 0:
			#hash = hash*255/hash_cnt
		    	hash = np.asarray(hash,np.uint32)
		    	img_label = np.asarray(img_label,np.uint32)
		    	output = hash[img_label]
		    	self.label = hash_cnt
			self.labe_arr = np.zeros((hash_cnt, max_L,2), np.int32)
			self.labe_cnt = np.zeros(hash_cnt,np.int32)
			self.start_point = np.zeros((hash_cnt,2),np.int32)
			self.last_point = np.zeros((hash_cnt, 2), np.int32)
			for i in range(hash_cnt):
				self.start_point.itemset(i,0,stats.item(index_list[i],0))
				self.start_point.itemset(i,1,stats.item(index_list[i],1))
				self.last_point.itemset(i,0, stats.item(index_list[i],0) + stats.item(index_list[i],2))
				self.last_point.itemset(i,1, stats.item(index_list[i],1) + stats.item(index_list[i],3))
				self.labe_cnt.itemset(i,stats.item(index_list[i],2)+1)
			labe_flag = np.zeros(hash_cnt,np.int32)
			flag_cnt = 0
			for x in range(0,width):
				y = height - 1
			    	labe_flag[:] = 0
			    	flag_cnt = 0
			    	while y >= 0 :
					h_val = output.item(y,x)
					if h_val != 0 :
						if labe_flag.item(h_val - 1) == 0 and flag_cnt<hash_cnt:
						    	labe_flag.itemset(h_val-1,1)
						    	flag_cnt += 1
							self.labe_arr.itemset(h_val-1,self.labe_cnt.item(h_val-1)-1,0,x)
							self.labe_arr.itemset(h_val-1,self.labe_cnt.item(h_val-1)-1,1,y)
					y -= 1
			output = output*255/hash_cnt
			output = np.array(output,np.uint8)
			str = "hash_cnt : %d" %hash_cnt
     	 		cv2.putText(output, str, (0,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255))
		return output
