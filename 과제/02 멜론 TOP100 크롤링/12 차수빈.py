#!/usr/bin/env python
# coding: utf-8

# In[53]:


import requests as req #페이지의 정보 요청하는 라이브러리인 request import


# In[54]:


res = req.get("https://www.melon.com/chart/index.htm")
res # get함수를 불러 멜론 페이지 요청했지만 안됨...


# In[55]:


h = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
# 속이자, 딕셔너리 형식으로 묶기!


# In[56]:


res = req.get("https://www.melon.com/chart/index.htm", headers=h) # headers로 h딕셔너리 받기


# In[57]:


res # 페이지 가지고 옴.


# In[101]:


res.text # Melon 페이지 정보 확인


# In[102]:


import requests
from bs4 import BeautifulSoup # request, BeautifulSoup 모듈 import


# In[103]:


soup


# In[83]:


singer = soup.select("span.checkEllipsis") # 가수 불러오기


# In[84]:


singer


# In[85]:


len(singer) #top 100 가수


# In[86]:


singer[0].text #가수 이름만 추출


# In[87]:


for i in singer:
    print(i.text) #top100가수 불러오기


# In[108]:


song = soup.select("div.rank01>span")
album = soup.select("div.pd_1_12>tr")


# In[114]:


for i in album:
    print(i.text.strip())


# In[109]:


for i in song:
    print(i.text)


# In[90]:


for i in song:
    print(i.text.strip())


# In[91]:


import pandas as pd


# In[92]:


song_list = [] # 노래제목(텍스트) 리스트
singer_list = [] # 가수명(텍스트) 리스트
rank_list = [] # 순위 리스트

for i in range(len(song)):
    
    song_list.append(song[i].text.strip())
    singer_list.append(singer[i].text.strip())
    rank_list.append(i+1)


# In[93]:


print(song_list)


# In[94]:


print(singer_list)


# In[95]:


info = {"rank" : rank_list,"singer":singer_list, "title":song_list}


# In[96]:


music = pd.DataFrame(info)


# In[97]:


music.set_index('rank', inplace = True )


# In[98]:


music


# In[ ]:





# In[ ]:




