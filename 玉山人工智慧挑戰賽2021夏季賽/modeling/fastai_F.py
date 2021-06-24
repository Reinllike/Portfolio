#!/usr/bin/env python
# coding: utf-8

# In[1]:


import fastai
from fastai import *
from fastai.vision import *
from fastai.vision.all import *
import torch
from fastai import vision


# In[2]:


from fastai import *
from fastai.vision import *
from fastai.vision.all import *
data = ImageDataLoaders.from_folder(path, valid_pct=0.2, size=100*100)
learn =cnn_learner(data, models.resnet101, metrics=accuracy ).to_fp16()  
learn.load(r'resnetF101_6_all2_2')


# In[3]:


from fastai.vision import augment


# In[21]:


tfms = aug_transforms(max_rotate=180)
#plt.subplots(2,4,figsize=(12,8))


# In[5]:


tfms=DihedralItem()


# In[19]:


fig, axs = plt.subplots(1,4,figsize=(8,2))
for k, ax in enumerate(axs.flatten()):
    DihedralItem.encodes(get_ex(), k).show(ax=ax, title=f'k={k}')
plt.tight_layout()


# In[2]:



matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #'Heit'
#path=r'C:\Users\e921e\Esun_AI\model\pic_data\generate'
data = ImageDataLoaders.from_folder(r'C:\Users\e921e\Esun_AI\model\pic_data\pic1600', valid_pct=0.2, size=100 ,bs=64)
print(data)
train_ds = data.train_ds  # 取出训练集
valid_ds = data.valid_ds


# In[ ]:


data.train_ds 


# # 生成模型

# In[14]:


#learn = unet_learner(data, models.resnet18, metrics=accuracy ).to_fp16()


# In[4]:


# 拉取数据
#data = ImageDataLoaders.from_folder(untar_data(URLs.MNIST_SAMPLE))
learn =cnn_learner(data, models.resnet101, metrics=accuracy ).to_fp16() #

# 使用learn的fit方法就可以进行训练了，训练一遍
#learn.fit(1)


# In[5]:


learn.load(r'resnet1600F_34_22_1')


# # 訓練

# In[4]:


learn.lr_find()


# In[14]:


learn.fine_tune(1, 1e-3)


# In[9]:


learn.fit_one_cycle(1,0.01)


# In[27]:


learn.precompute = False 
learn.unfreeze()
#learn.lr_find()


# In[28]:


learn.fit_one_cycle(1,lr_max=slice(1e-7,1e-4 ))


# In[19]:


learn.precompute = True
learn.freeze()
#learn.lr_find()


# In[20]:



learn.fit_one_cycle(1,0.003)


# In[16]:


def get_dls(bs, size):
    dblock = DataBlock(blocks = (ImageBlock, CategoryBlock),
                       get_items = get_image_files,
                       get_y = parent_label,
                       splitter = GrandparentSplitter(),
                       item_tfms = Resize(size)
                      )
    return dblock.dataloaders(path, bs = bs)


# In[43]:


learn.fit_one_cycle(1, 1e-3)


# In[21]:


learn.save(r'resnet1600F_34_22_1')


# # 訓練結果

# In[18]:


learn.summary()


# In[22]:


#learn.plot_multi_top_losses(9,figsize=(6,6))


# In[6]:


interp=Interpretation.from_learner(learn)
interp.top_losses(9)


# In[7]:


interp.plot_top_losses(9,figsize=(6,6))


# In[8]:


inter=ClassificationInterpretation.from_learner(learn)
#inter.plot_confusion_matrix(9)
inter.confusion_matrix()


# # 取得預測valid機率值 排序

# In[13]:


lgp=learn.get_preds()


# In[23]:


li=[]
li2=[]
li3=[]

for i in range(0,len(lgp[1])):
    a=lgp[0][i]
    y = sorted(a, reverse = True)
    li.append(y[0])
    li2.append(y[1])
    li3.append(y[2])
    


# In[18]:


lgp


# In[24]:


x = sorted(li)
y = sorted(li2)
z = sorted(li3)



# In[31]:


u=int(len(x)*0.02)
x[u]


# In[26]:


u=int(len(x)*0.999)
y[u]


# In[27]:


u=int(len(x)*0.999)
z[u]


# In[33]:


ten10


# # 判斷機率值小於閥值 = 'isnull'

# In[5]:


def Prob_judgment(img):
    ten10=learn.predict(img)
    word=ten10[0]

    if ten10[2][ten10[1]]>0.5:
        return(word)
    else :
        return('isnull')


# In[8]:


import cv2
path = r'C:\Users\e921e\Esun_AI\model\pic_data\41191.jpg' 
img_gray = cv2.imread(path , 0)
Prob_judgment(img_gray)


# In[5]:


import cv2
from keras.preprocessing import image
path = (r'C:\Users\e921e\Esun_AI\dataclean\second\0_戶.jpg' )
img = image.load_img(path,color_mode = "grayscale")
img_array = image.img_to_array(img)
        
ret,th1 = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)
res_img = cv2.resize(th1,(100,100),interpolation = cv2.INTER_CUBIC)
#learn.predict(res_img )[0]

#cv2.imshow("res_img", res_img)
#cv2.waitKey()
#cv2.destroyAllWindows()
#learn.predict(res_img)


# In[26]:


img


# In[89]:


import torch
import torchvision.models as models

torch_model =torch.load(r'C:\Users\e921e\Esun_AI\model\fastai_res101.pth')# pytorch模型加载

#model = models.resnet101()
#model.fc = torch.nn.Linear(2048, 4)
#model.load_state_dict(torch_model) 

batch_size = 1  #批处理大小
input_shape = (5, 100, 100)   #输入数据,改成自己的输入shape

# #set the model to inference mode

x = torch.randn(batch_size, *input_shape)	# 生成张量
export_onnx_file = "test.onnx"			# 目的ONNX文件名
torch.onnx.export(model,
                    x,
                    export_onnx_file,
                    opset_version=10,
                    do_constant_folding=True,	# 是否执行常量折叠优化
                    input_names=["input"],	# 输入名
                    output_names=["output"],	# 输出名
                    dynamic_axes={"input":{0:"batch_size"},  # 批处理变量
                                    "output":{0:"batch_size"}})


# In[46]:


#權重
learn.state_dict() 


# In[ ]:




