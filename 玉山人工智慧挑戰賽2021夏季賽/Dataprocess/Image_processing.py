#!/usr/bin/env python
# coding: utf-8

# In[9]:


import cv2
import numpy as np
from PIL import Image

#讀取影像
image = cv2.imread(r'C:\Users\e921e\Esun_AI\dataclean\first\13.jpg',cv2.IMREAD_COLOR)
img = cv2.imread(r'C:\Users\e921e\Esun_AI\dataclean\first\13.jpg',0)
cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()


# In[38]:


#查看原始圖片size大小
size = image.shape
sz1 = size[0] #height(rows) of image
sz2 = size[1] #width(colums) of image
sz3 = size[2] #the pixels value is made up of three primary colors
print ( 'width: %d \nheight: %d \nnumber: %d' %(sz1,sz2,sz3) )


# In[8]:


import numpy as np
data = np.array(li)


# In[9]:


data


# In[10]:


#縮放成 300*300
res_img = cv2.resize(image,(200,200),interpolation = cv2.INTER_CUBIC)
cv2.imshow("res_img", res_img)
cv2.waitKey()
cv2.destroyAllWindows()


# In[11]:


#查看resize後圖片size大小
size = res_img.shape
sz4 = size[0] #height(rows) of image
sz5 = size[1] #width(colums) of image
sz6 = size[2] #the pixels value is made up of three primary colors
print ( 'width: %d \nheight: %d \nnumber: %d' %(sz4,sz5,sz6) )


# In[15]:


#灰階
gray_img = cv2.cvtColor(res_img , cv2.COLOR_RGB2GRAY)
cv2.imshow("gray_img", gray_img)
cv2.waitKey()
cv2.destroyAllWindows()


# In[18]:


gray_img


# In[5]:


#二值化反轉
#sim_inv = cv2.threshold(gray_img, 110 , 255 , cv2.THRESH_BINARY_INV)[1]
#cv2.imshow("sim_inv", sim_inv)

#ret,th1 = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
#cv2.imshow("sim_inv", th1)

ret,sim_inv = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #cv2.THRESH_BINARY_INV
cv2.imshow('binary image', sim_inv)
    
cv2.waitKey()
cv2.destroyAllWindows()


# In[33]:


#模糊化
mblur = cv2.medianBlur(sim_inv,3)
cv2.imshow("mblur", mblur)
cv2.waitKey()
cv2.destroyAllWindows()


# In[34]:


#開運算
kernel = np.ones( (2,2) , np.uint8 )
open_img = cv2.morphologyEx(mblur , cv2.MORPH_OPEN , kernel)
cv2.imshow("mblur", open_img)
cv2.waitKey()
cv2.destroyAllWindows()


# In[38]:



#cv2.imshow("article", image)
#cv2.imshow("res_img", res_img)
cv2.imshow("gray_img", gray_img)
cv2.imshow("sim_inv", sim_inv)
cv2.imshow("mblur", mblur)
cv2.imshow("mb2", open_img)
cv2.waitKey()
cv2.destroyAllWindows()


# In[37]:


#灰階 => 二值化
import cv2
import matplotlib.pyplot as plt

#img = cv2.imread('flower.jpg',0) #直接读为灰度图像
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,2) #换行符号 \
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,10) #换行符号 \
images = [img,th1,th2,th3]
plt.figure()
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
plt.show()


# In[48]:


from skimage import data, io, filters

image = data.coins()

# … or any other NumPy array!

edges = filters.sobel(image)

io.imshow(edges)


io.show()


# In[62]:


#抓單字位置
from __future__ import print_function

#下方的步驟中, 我們使用skimage提供的Adaptive threshold而非OpenCV


#Connected-component labeling相關功能就放在skimage的子模組measure

from skimage import measure

import numpy as np

import cv2

#載入圖片並模糊化處理

plate = cv2.medianBlur(image, 5)

#將圖片由RGB轉為HSV格式，然後取HSV中的Ｖ值，此效果與灰階效果類似。


#使用skimage提供的Adaptive threshold


ret,thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


# In[67]:


labels = measure.label(thresh, neighbors=8, background=0)


# In[69]:


mask = np.zeros(thresh.shape, dtype='uint8')


# In[71]:


print('[INFO] Total {} blobs'.format(len(np.unique(labels))))


# In[103]:


for (i, label) in enumerate(np.unique(labels)):

        #如果label=0，表示它為背景

    if label == 0:

        print('[INFO] label: 0 (background)')

        continue

        #否則為前景，顯示其label編號l

    print('[INFO] label: {} (foreground)'.format(i))
    
    labelMask = np.zeros(thresh.shape, dtype='uint8')

    labelMask[labels == label] = 255 


        #有幾個非0的像素?

    numPixels = cv2.countNonZero(labelMask)

    if numPixels > 50 and numPixels < 5000:

                          #放到剛剛建立的空圖中

        mask = cv2.add(mask, labelMask)


# In[90]:


labelMask = np.zeros(thresh.shape, dtype='uint8')

labelMask[labels == label] = 255


        #有幾個非0的像素?

numPixels = cv2.countNonZero(labelMask)

if numPixels > 2 and numPixels < 40:

                          #放到剛剛建立的空圖中

    mask = cv2.add(mask, labelMask)


# In[105]:


#if numPixels > 2 and numPixels < 40:

                          #放到剛剛建立的空圖中

   # mask = cv2.add(mask, labelMask)

#顯示該前景物件

cv2.imshow('Label', labelMask)

cv2.waitKey(0)

#顯示所抓取到的車牌

cv2.imshow('Large Blobs', mask)

cv2.waitKey(0)


# In[119]:


y=[x for x in range(1,15)]
y


# In[ ]:


S4=
S5 = {x for x in range(8,17)} & S4


# In[117]:


list2=[]
for i in range(1,15):
    list2.append(i)
list2


# In[ ]:


for i in S4:
    if i >15 & i<25:
        S5.append(i)


# In[1]:


S5 = {x for x in S4 if 7<x<17}


# In[ ]:




