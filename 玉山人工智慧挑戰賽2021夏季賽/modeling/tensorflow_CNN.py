#!/usr/bin/env python
# coding: utf-8

# In[1]:



import matplotlib.pyplot as plt

import pandas as pd

import numpy as np

from keras.utils import np_utils

import os

from keras.preprocessing import image

from tensorflow.keras.models import Sequential 

import tensorflow as tf

from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D ,BatchNormalization

import cv2
path=r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data/'
allFileList = os.listdir(path)
allFileList
images = []
labels = []
for i in allFileList:
    #path = ('pic_data\generate\%s/' %i)
    path2 =  path+i+'/'
    files = os.listdir(path2)    
    for j in files:
        imgpath=path2+j
        img = image.load_img(imgpath) #,color_mode = "grayscale"
        img_array = image.img_to_array(img)
        
        images.append(img_array)
        
        #lb=i
        #labels.append(lb)
data = np.array(images)
#labels = np.array(labels)

#for i in range(0,800):
 #   for j in range(0,25):
  #      labels.append(i)
#labels = np.array(labels)

cnt=0
for i in os.listdir(path):
    #print(i)
    #num_dirs += 1
    path2 = path + "\\" + i
    for j in os.listdir(path2):
        labels.append(cnt)
    cnt+=1
labels = np.array(labels)
#print(num_dirs)


# In[3]:


import numpy as np
import random
def shuffle(*args):
    seed = random.randint(0,2**32)
    rand_state = np.random.RandomState(seed)
    for i in args:
        rand_state.shuffle(i)
        rand_state.seed(seed) 
shuffle(li,li2,li3)


# In[2]:


li=[2,6,8]
li2=[24,65,86]
li3=['a','f','r']


# In[6]:


li3


# In[7]:


li4=[1,2,3]
shuffle(li4)


# In[3]:


data /= 255


# In[4]:


from sklearn.model_selection import train_test_split

(x_train, x_test, y_train, y_test) = train_test_split(data, labels, test_size=0.2)

X_train = x_train.reshape(x_train.shape[0], 100, 100, 3).astype('float32')

X_test = x_test.reshape(x_test.shape[0], 100, 100, 3).astype('float32')

print('X_train.shape={}, y_train.shape={}'.format(X_train.shape, y_train.shape))

print('X_test.shape={}, y_test.shape={}'.format(X_test.shape, y_test.shape))


# In[5]:


y_train = np_utils.to_categorical(y_train)

y_test_categories = y_test

y_test = np_utils.to_categorical(y_test)


# In[ ]:


keras.applications.resnet.ResNet101(include_top=True, weights='imagenet', input_tensor=None, input_shape=(100,100,1), 
                                    pooling=None, classes=1000)


# In[37]:


from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(include_top=False,pooling='avg',input_shape=(100,100,3))
model.summary()


# In[10]:


from tensorflow.python.keras.models import Model
x = model.output
x = Flatten()(x)
x = Dropout(0.5)(x)

# 增加 Dense layer，以 softmax 產生個類別的機率值
output_layer = Dense(801, activation='softmax', name='softmax')(x)

# 設定凍結與要進行訓練的網路層
net_final = Model(inputs=model.input, outputs=output_layer)
for layer in net_final.layers[:-7]:
    layer.trainable = False
for layer in net_final.layers[-7:]:
    layer.trainable = True


# In[11]:


from tensorflow.python.keras import models


# In[12]:


net_final.summary()


# In[40]:


net_final.layers[-1]


# In[43]:


model.layers.pop()


# In[11]:


model = Sequential([
    Dense(16, input_shape=(1,5), activation='relu'),
    BatchNormalization(),
    Dense(32, activation='relu'),
    BatchNormalization(),
    Dense(2, activation='softmax')
])


# In[10]:


model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(2, 2), padding='same', input_shape=(100, 100, 1), activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(2, 2), padding='same', activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(800, activation='softmax'))

model.summary()   


# In[31]:


Adam=tf.keras.optimizers.Adam(learning_rate=0.03, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.00, amsgrad=False)
#Adam=tf.keras.optimizers.Adamax(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.001) 
#Adam = tf.keras.optimizers.SGD(lr=0.001, decay=0.0001, momentum=0.5, nesterov=True)


# In[32]:


net_final.compile(loss='categorical_crossentropy', optimizer=Adam, metrics=['accuracy'])


# In[36]:


train_history=net_final.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), validation_split=0.2, epochs=3
                            , batch_size=80, verbose=2)


# In[ ]:





# In[21]:


net_final = models.load_model( r'C:\Users\e921e\Esun_AI\model\pic_data\resnet50_all17.h5')


# In[25]:


model.save(
    r'C:\Users\e921e\Esun_AI\model\pic_data\resnet50_all17.h5'
)


# In[ ]:


def show_train_history(train_history, train, validation):

    plt.plot(train_history.history[train])

    plt.plot(train_history.history[validation])

    plt.title('Train History')

    plt.ylabel('train')

    plt.xlabel('Epoch')

    plt.legend(['train', 'validation'], loc='center right')

    plt.show()


# In[ ]:


show_train_history(train_history,'accuracy','val_accuracy')


# In[ ]:


show_train_history(train_history, 'loss','val_loss')


# In[ ]:


scores = model.evaluate(X_test, y_test)

scores[1]


# In[ ]:


prediction = np.argmax(model.predict(X_test), axis=-1)
print(y_test.shape)

pd.crosstab(y_test_categories, prediction, rownames=['label'], colnames=['predict'])

