#!/usr/bin/env python
# coding: utf-8

# # 檔名轉成數字

# In[46]:


#檔案重新命名
import os
path = r"C:\Users\e921e\Esun_AI\train2/"
# 獲取該目錄下所有檔案，存入列表中
f = os.listdir(path)

n = 0
i = 0
for i in f:
    # 設定舊檔名（就是路徑+檔名）
    oldname = f[n]

    # 設定新檔名
    newname = str(n+1) + '.jpg'
    # 用os模組中的rename方法對檔案改名
    os.rename(path+oldname, path+newname)
    print(oldname, '======>', newname)

    n += 1


# # 圖片處理

# In[18]:



def process_image(img, min_side):
    size = img.shape
    h, w = size[0], size[1]
    #长边缩放为min_side
    scale = max(w, h) / float(min_side)
    new_w, new_h = int(w/scale), int(h/scale)
    resize_img = cv2.resize(img, (new_w, new_h))
    # 填充至min_side * min_side
    if new_w % 2 != 0 and new_h % 2 == 0:
        top, bottom, left, right = (min_side-new_h)/2, (min_side-new_h)/2, (min_side-new_w)/2 + 1, (min_side-new_w)/2
    elif new_h % 2 != 0 and new_w % 2 == 0:
        top, bottom, left, right = (min_side-new_h)/2 + 1, (min_side-new_h)/2, (min_side-new_w)/2, (min_side-new_w)/2
    elif new_h % 2 == 0 and new_w % 2 == 0:
        top, bottom, left, right = (min_side-new_h)/2, (min_side-new_h)/2, (min_side-new_w)/2, (min_side-new_w)/2
    else:
        top, bottom, left, right = (min_side-new_h)/2 + 1, (min_side-new_h)/2, (min_side-new_w)/2 + 1, (min_side-new_w)/2
 
    pad_img = cv2.copyMakeBorder(resize_img, int(top), int(bottom), int(left), int(right), cv2.BORDER_CONSTANT, value=[255,255,255]) #从图像边界向上,下,左,右扩的像素数目
    return pad_img


# In[48]:


#圖片處理
import numpy as np
import cv2
import os
path = r"C:\Users\e921e\Esun_AI\train2/"
pathw =r'C:\Users\e921e\Esun_AI\train3/'
f = os.listdir(path)
kernel = np.ones( (2,2) , np.uint8 )
n=1
for u in f:
    imgpath=path+u
    img = cv2.imread(imgpath,0)
    
    #二值化
    #ret,img = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
    ret,img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #sim_inv = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C ,\
#cv2.THRESH_BINARY,71,40)

    #橫線刪除    
    img=img
    for i in range(0,67):
        if sum(img[i]) < len(img[i])*20:
            for j in range(len(img[i])):
                img[i][j]=255
    
    #直線刪除
    for j in range(len(img[i])):
        c=0
        for i in range(0,67):       
            c+=img[i][j]
        if c < 67*30:
            for i in range(0,67):       
                img[i][j]=255
    
          
  
    #模糊化 
    img = cv2.medianBlur(img,3)
    
     #開運算
    img = cv2.morphologyEx(img , cv2.MORPH_OPEN , kernel)    
    
                
    #圖片填滿 改變SIZE
    img=process_image(img,100)
    

                 
    #存入
    name = u 
    cv2.imwrite(pathw+name, img)
    
    n += 1
    
    


# # 檔名回復

# In[49]:


#檔名回復
import os
path = r"C:\Users\e921e\Esun_AI\train/"
pathn= r'C:\Users\e921e\Esun_AI/train3/'
# 獲取該目錄下所有檔案，存入列表中
f = os.listdir(path)

n = 0
i = 0
for i in f:
    # 設定舊檔名（就是路徑+檔名）
    oldname = f[n]

    # 設定新檔名
    newname = str(n+1) + '.jpg'
    # 用os模組中的rename方法對檔案改名
    os.rename(pathn+newname, pathn+oldname)

    n += 1


# # Test

# In[84]:


#圖片處理
import numpy as np
import cv2
import os
path = r"C:\Users\e921e\Esun_AI\dataclean\first/"
pathw =r'C:\Users\e921e\Esun_AI\dataclean\Third/'
f = os.listdir(path)
kernel = np.ones( (2,2) , np.uint8 )
n=1
for i in f:
    imgpath=path+i
    img = cv2.imread(imgpath,0)
    #二值化
    #ret,img = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
    ret,img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #sim_inv = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C ,\
#cv2.THRESH_BINARY,71,40)
    #模糊化
   # img = cv2.medianBlur(img,1)
    
    #開運算
 #   img = cv2.morphologyEx(img , cv2.MORPH_OPEN , kernel)
    
    #橫線刪除
    img=img
  #  for i in range(0,67):
   #     if sum(img[i]) < len(img[i])*20:
    #        for j in range(len(img[i])):
     #           img[i][j]=255
                
    #圖片填滿 改變SIZE
    img=process_image(img,100)
    
    #存入
    name = i + '.jpg'
    cv2.imwrite(pathw+name, img)
    
    n += 1


# In[ ]:





# # 檔案歸檔

# In[52]:


import cv2

import pandas as pd

import numpy as np

import os

path=r'C:\Users\e921e\Esun_AI\model\pic_data\generate/' #檔案放入
pathw=r'C:\Users\e921e\Esun_AI\train3/' #取出檔案

allFileList = os.listdir(path)
allFileList2 = os.listdir(pathw)
n=100
for u in allFileList2: #取出檔案
    pic1 = pathw+u
    
    for i in allFileList: #歸檔位置
        if i in u: 
            path2 = path+i
            os.rename(pic1, path2+'/'+str(n)+'.jpg') #舊轉新名 放入
            
            n+=1
         


# In[42]:


path=r'C:\Users\e921e\Esun_AI\model\pic_data\generate/'
pathw=r'C:\Users\e921e\Esun_AI\dataclean\second/'
allFileList = os.listdir(path)
allFileList2 = os.listdir(pathw)
li=allFileList.copy()

for o in allFileList:
    for p in allFileList2:
        if o in p:
            try:
                li.remove(o)
            except:
                pass
li


# In[44]:


path=r'C:\Users\e921e\Esun_AI\model\pic_data\generate/'
pathw=r'C:\Users\e921e\Esun_AI\dataclean\second/'
allFileList = os.listdir(path)
allFileList2 = os.listdir(pathw)

ll=['ewe','三','丁','曾']
for o in allFileList:
    for p in allFileList2:
        if o in p:
            try:ll.remove(o)
            except:
                pass
            
ll


# # 創建資料夾

# In[4]:


allFileList = os.listdir(r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data')


# In[5]:


import os
path = r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data_trans/'
for i in allFileList:
    os.mkdir(path+i)


# # 數據增強_旋轉 *4

# In[9]:


from cv2 import rotate
rotate1=rotate(img_array,90)
rotate1


# In[1]:


import cv2
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    #cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img


# In[6]:


import cv2
#from cv2 import rotate
import os
import numpy as np

path1 = r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data'
path8 = r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data_trans'
for i in os.listdir(path1): # i=字 檔名
    #print(i)
    #num_dirs += 1
    path2 = path1 + "\\" + i
    for j in os.listdir(path2):#每張圖片
        path3 = path2 + '\\' +j
        
        img = cv_imread(path3)
        img1 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img2 = cv2.rotate(img, cv2.ROTATE_180)
        img3 = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        cv2.imencode('.jpg',img)[1].tofile(path8 + '\\' + i + '\\' + j + '.jpg')
        cv2.imencode('.jpg',img1)[1].tofile(path8 + '\\' + i + '\\' + j + '_1.jpg')
        cv2.imencode('.jpg',img2)[1].tofile(path8 + '\\' + i + '\\' + j + '_2.jpg')
        cv2.imencode('.jpg',img3)[1].tofile(path8 + '\\' + i + '\\' + j + '_3.jpg')
        


# In[12]:


import cv2
#from cv2 import rotate
import os
import numpy as np
img = cv_imread(r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data\丁\0.jpg')
cv2.imencode('.jpg',img)[1].tofile(r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data_trans\丁\5.jpg')


# In[8]:


img


# In[35]:


import numpy as np
import cv2

imgpath=r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data\丁\0.jpg'
img = cv_imread(imgpath)
img1 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
img2 = cv2.rotate(img, cv2.ROTATE_180)
img3 = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)

#name = i + '.jpg'

cv2.imwrite(r'C:\Users\e921e\Esun_AI\model\pic_data\0.jpg', img)
cv2.imwrite(r'C:\Users\e921e\Esun_AI\model\pic_data\0_1.jpg', img1)
cv2.imwrite(r'C:\Users\e921e\Esun_AI\model\pic_data\0_2.jpg', img2)
cv2.imwrite(r'C:\Users\e921e\Esun_AI\model\pic_data\0_3.jpg', img3)

#cv2.imshow("img", img1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# # 取隨機isnull label

# In[108]:


import pandas as pd
df = pd.read_table('480810.txt')  


# In[114]:


for i in lll:
    rr=i


# In[113]:


lll=['先回則任取據處隊南給色光門即保治北造百規熱領七海地口東導器壓志世金增爭濟階油思術極交受聯什認六共權收證改清已美再採轉更單風切打白教速花帶安場身車例真務具萬每目至達走積示議聲報鬥完類八離華名確才科張信馬節話米整空元況 今集溫傳土許步群廣石記需段研界拉林律叫且究觀越織裝影算低持音眾書布復容兒須際商非驗連斷深難近礦千周委素技備半辦青省列習響約支般史感勞便團往酸歷市 克何除消構府稱太準精值號率族維劃選標寫存候毛親快效斯院查江型眼王按格養易置派層片始卻專狀育廠京識適屬圓包火住調滿縣局照參紅細引聽該鐵價嚴首底液官 德調隨病蘇失爾死講配女黃推顯談罪神藝呢席含企望密批營項防舉球英氧勢告李台落木幫輪破亞師圍注遠字材排供河態封另施減樹溶怎止案言士均武固葉魚波視僅費 緊愛左章早朝害續輕服試食充兵源判護司足某練差致板田降黑犯負擊範繼興似餘堅曲輸修的故城夫夠送筆船佔右財吃富春職覺漢畫功巴跟雖雜飛檢吸助昇陽互初創抗 考投壞策古徑換未跑留鋼曾端責站簡述錢副盡帝射草衝承獨令限阿宣環雙請超微讓控州良軸找否紀益依優頂礎載倒房突坐粉敵略客袁冷勝絕析塊劑測絲協重訴念陳仍 羅鹽友洋錯苦夜刑移頻逐靠混母短皮終聚汽村雲哪既距衛停烈央察燒行迅境若印洲刻括激孔搞甚室待核校散侵吧甲遊久菜味舊模湖貨損預阻毫普穩乙媽植息擴銀語揮 酒守拿序紙醫缺雨嗎針劉啊急唱誤訓願審附獲茶鮮糧斤孩脫硫肥善龍演父漸血歡械掌歌沙著剛攻謂盾討晚粒亂燃矛乎殺藥寧魯貴鐘煤讀班伯香介迫句豐培握蘭擔弦蛋 沉假穿執答樂誰順煙縮徵臉喜松腳困異免背星福買染井概慢怕磁倍祖皇促靜補評翻肉踐尼衣寬揚棉希傷操垂秋宜氫套筆督振架亮末憲慶編牛觸映雷銷詩座居抓裂胞呼 娘景威綠晶厚盟衡雞孫延危膠還屋鄉臨陸顧掉呀燈歲措束耐劇玉趙跳哥季課凱胡額款紹卷齊偉蒸殖永宗苗川爐岩弱零楊奏沿露桿探滑鎮飯濃航懷趕庫奪伊靈稅了途滅 賽歸召鼓播盤裁險康唯錄菌純藉糖蓋橫符私努堂域槍潤幅哈竟熟蟲澤腦壤碳歐遍側寨敢徹慮斜薄庭都納彈飼伸折麥濕暗荷瓦塞床築惡戶訪塔奇透梁刀旋跡卡氯遇份毒泥退洗擺灰彩賣耗夏擇忙銅獻硬予繁圈雪函亦抽篇陣陰丁尺追堆雄迎泛爸樓避謀噸野豬旗累偏典館索秦脂潮爺豆忽托驚塑遺愈朱替纖粗傾尚痛楚謝奮購磨君池旁碎骨 監捕弟暴割貫殊釋詞亡壁頓寶午塵聞揭砲殘冬橋婦警綜招吳付浮遭徐您搖谷贊箱隔訂男吹樂園紛唐敗宋玻巨耕坦榮閉灣鍵凡駐鍋救恩剝凝鹼齒截煉麻紡禁廢盛版緩淨 睛昌婚涉筒嘴插岸朗莊街藏姑貿腐奴啦慣乘夥恢勻紗扎辯耳彪臣億璃抵脈秀薩俄網舞店噴縱寸汗掛洪著賀閃柬爆烯津稻牆軟勇像滾釐蒙芳肯坡柱盪腿儀旅尾軋冰貢登黎削鑽勒逃障氨郭峰幣港伏軌畝畢擦莫刺浪秘援株健售股島甘泡睡童鑄湯閥休匯舍牧繞炸哲磷績朋淡尖啟陷柴呈徒顏淚稍忘泵藍拖洞授鏡辛壯鋒貧虛彎摩泰幼廷尊窗綱弄隸疑氏宮姐震瑞怪尤琴循描膜違夾腰緣珠窮森枝竹溝催繩憶邦剩幸漿欄擁牙貯禮濾鈉紋彈罷拍咱喊袖埃勤罰焦潛伍墨欲縫姓刊飽仿獎鋁鬼麗跨默挖鏈掃喝袋炭污幕諸弧勵梅奶潔災舟鑑苯訟抱毀率懂寒智埔寄屆躍渡挑丹艱貝碰拔爹戴碼夢芽熔赤漁哭敬顆奔藏鉛熟仲虎稀妹乏珍申桌遵允隆螺倉魏銳曉氮兼隱礙赫撥忠肅缸牽搶博 巧殼兄杜訊誠碧祥柯頁巡矩悲灌齡倫票尋桂鋪聖恐恰鄭趣抬荒騰貼柔滴猛闊輛妻填撤儲簽鬧擾紫砂遞戲吊陶伐餵療瓶婆撫臂摸忍蝦蠟鄰胸鞏擠偶棄槽勁乳鄧吉仁爛磚 租烏艦伴瓜淺丙暫燥橡柳迷暖牌纖秧膽詳簧踏瓷譜呆賓糊洛輝憤競隙怒粘乃緒肩籍敏塗熙皆偵懸掘享糾醒狂鎖澱恨牲霸爬賞逆玩陵祝秒浙貌役彼悉鴨著趨鳳晨畜輩秩 卵署梯炎灘棋驅篩峽冒啥壽譯浸泉帽遲硅疆貸漏稿冠嫩脅芯牢叛蝕奧鳴嶺羊憑串塘繪酵融盆錫廟籌凍輔攝襲筋拒僚旱鉀鳥漆']


# In[121]:


from re import compile as _Re
for i in lll:
    print(5)
_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split
def split_unicode_chrs( text ):
    return [ chr for chr in _unicode_chr_splitter( text ) if chr ]


# In[122]:


rr=split_unicode_chrs(i)


# In[65]:


li=[]
for i in range(0,int(len(df['常用字'])/3)):
    li.append(df['常用字'][i])


# In[126]:


li3=[]
rr2=rr.copy()


# In[130]:


import os
li2=[]
path=r'C:\Users\e921e\Esun_AI\model\pic_data\pic_data'
li2=os.listdir(path)


# In[134]:


for i in rr:
    for j in li2:
        if i == j:
            rr2.remove(i)


# In[136]:


f = open('480811.txt', 'a+',encoding="utf-8")
for u in range(0,len(rr2)):
    r=rr2[u]
    f.write(r)
f.close()


# In[79]:


f.close()


# # 抓文字框框

# In[186]:


import cv2

path=r'C:\Users\e921e\Esun_AI\model\pic_data\41191.jpg'

img = cv2.imread(path,0)

blurred = cv2.GaussianBlur(img, (5, 5), 0)

binaryIMG = cv2.Canny(blurred, 5, 40)

contours, hierarchy = cv2.findContours(binaryIMG, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
 
for bbox in bounding_boxes:
    [x , y, w, h] = bbox
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("name", img)
cv2.waitKey(0)


# In[188]:


count=0
word=[]
def words(b,count):
    a=len(contours[count])
    if a > b:
        b=a
        word.append(count)
    
    count+=1
    if count < len(contours):
        words(b,count)
        
words(0,0)    
contours[word[-1]]


# In[ ]:




