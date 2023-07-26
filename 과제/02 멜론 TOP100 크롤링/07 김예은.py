#!/usr/bin/env python
# coding: utf-8

# In[89]:


import datetime


# In[3]:


published_dalta = "10분전" # 8시간전, 9분전

published_at = datetime.datetime.now()

if "일전" in published_dalta :
    days = int(published_dalta.replace("일전", ""))
    published_at -= datetime.timedelta(days=days)
elif "시간전" in published_dalta :
    hours = int(published_dalta.replace("시간전", ""))
    published_at -= datetime.timedelta(hours=hours)
elif "분전" in published_dalta :
    minutes = int(published_dalta.replace("분전", ""))
    published_at -= datetime.timedelta(minutes=minutes)
else : # else를 빼먹지 않는다 !
    raise ValueError(f"지원하지 않는 포맷입니다. : {published_dalta}")
    
published_at


# In[ ]:


# 크롤링


# In[141]:


import requests
from bs4 import BeautifulSoup  
import pandas as pd


# In[91]:


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

url = "https://www.melon.com/chart/index.htm"
res = requests.get(url, headers=headers)
res


# In[92]:


html = res.text
soup = BeautifulSoup(html, "html.parser")

melon_tag_list = soup.select(".ellipsis.rank01 a")
melon_tag_list


# In[185]:


# 곡 일련번호 

# href 속성 값에서 곡 일련번호만 추출하여 song_id 변수에 저장
song_ids_list = []
for tag_id in soup.select('a[href*="playSong"]'):
    song_id = tag_id["href"].split(",")[1].strip(" ');")
    song_ids_list.append(song_id)

print(song_ids_list)


# In[147]:


# 앨범 

album = soup.select('.wrap .ellipsis.rank03 a')
album_list = []

for tag_album in album :
    album_list.append(tag_album.text)

len(album_list)


# In[148]:


# 곡명
title = soup.select('.wrap .ellipsis.rank01 a')
song_list = []

for song in title :
    song_list.append(song.text)
    
len(song_list)


# In[149]:


# 가수
singer = soup.select(".checkEllipsis")

singer_list = []
for tag_singer in singer :
    singer_list.append(tag_singer.text)
len(singer_list)


# In[173]:


# 커버이미지 주소

# 이미지 주소를 저장할 빈 리스트
add_list = []

# soup.select(".wrap a"): class가 "wrap"인 모든 요소에서 <a> 태그들을 선택합니다.
tag_add_list = soup.select(".wrap a")

# 모든 <a> 태그들에 대해 이미지의 src 값을 추출하여 add_list에 추가합니다.
for tag_add in tag_add_list:
    if tag_add.find("img"):
        image_src = tag_add.find("img")["src"]
        add_list.append(image_src)
len(add_list)



# In[189]:


# 좋아요

like_list = []

like = soup.select(".wrap a")
like


# In[188]:


df = pd.DataFrame(
    {
        '곡일련번호' : song_ids_list,
        '순위': range(1, 101),
        '앨범': album_list,
        '곡명': song_list,
        '가수': singer_list,
        '커버이미지_주소' : add_list,
    }
)

df.set_index('곡일련번호', inplace=True)

df

