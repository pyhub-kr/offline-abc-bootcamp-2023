#!/usr/bin/env python
# coding: utf-8

# In[20]:


import requests
from bs4 import BeautifulSoup


# In[21]:


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
}
url = "https://www.melon.com/chart/index.htm"

res = requests.get(url, headers=headers)
res


# In[22]:


html = res.text
html


# In[23]:


import re
import pandas as pd

def 멜론차트_가져오기():
    
    soup = BeautifulSoup(html, "html.parser")


    song_list_items = soup.select("div", class_="service_list_song type02 d_song_list") 
 
    song_title = []
    song_title_list = [] # 노래 제목 
    song_rank = []
    song_rank_list = [] # 순위
    album_list = [] # 앨범 명
    singer_list = [] # 가수 이름

    for song_list_item in song_list_items: 
        
        wrap_song_info = song_list_item.find("div", class_="wrap_song_info") 

        rank_info = song_list_item.find("span", class_="rank") 

        url_info = song_list_item.find("div", class_="wrap") 
        if rank_info:
            song_rank.append(rank_info.text)

        if wrap_song_info:

            ellipsis_rank01 = wrap_song_info.find("div", class_="ellipsis rank01") 
            ellipsis_rank02 = wrap_song_info.find("div", class_="ellipsis rank02") 
            ellipsis_rank03 = wrap_song_info.find("div", class_="ellipsis rank03") 

            if ellipsis_rank01:
                song_title.append(ellipsis_rank01.text.split('\n')[1]) 
                song_url = ellipsis_rank01.find("a")["href"] -

            if ellipsis_rank02:
                singer_name = ellipsis_rank02.find("span").text.strip() 
                                                                       
                singer_list.append(singer_name)
            if ellipsis_rank03:
                album_list.append(ellipsis_rank03.text.split('\n')[1])   

            wrap_song_info = ""

    song_title_list = list(dict.fromkeys(song_title))
    singer_list = singer_list[6:]

    for i in range(len(song_rank)):
        
        if song_rank[i] != "순위":
            song_rank_list.append(song_rank[i])
  
    j_url = "https://www.melon.com/commonlike/getSongLike.json?contsIds=36599950%2C36617841%2C36635522%2C36430773%2C36382580%2C36356993%2C36411344%2C36490426%2C36416114%2C36599949%2C34061322%2C36411342%2C36318125%2C35454426%2C36502910%2C34908740%2C35931532%2C35008524%2C35945927%2C36632907%2C36546894%2C35008525%2C32508053%2C35834583%2C35834584%2C36391236%2C35008527%2C36581408%2C36546895%2C35008534%2C35985167%2C35008528%2C35008526%2C35454425%2C35008531%2C32872978%2C35008532%2C36331121%2C33507137%2C36313117%2C35008530%2C34819473%2C35546497%2C35640751%2C30244931%2C36516320%2C8037843%2C36635524%2C35849863%2C36351997%2C36206259%2C36546900%2C33666269%2C34847378%2C36110996%2C36546908%2C36180700%2C36601157%2C36105548%2C36334401%2C36546897%2C36404853%2C35729104%2C36441862%2C36241824%2C36001290%2C36430774%2C36546902%2C36604256%2C34657844%2C4446485%2C36546899%2C36546903%2C36518341%2C36546905%2C36635523%2C36546906%2C36440243%2C35299693%2C33658563%2C36428682%2C36365073%2C34864406%2C34431086%2C35667692%2C36394038%2C34754292%2C36322781%2C36480197%2C35535827%2C35252996%2C35730562%2C36637828%2C36500102%2C36616378%2C33496587%2C36359275%2C36416116%2C35643794%2C36595401"
    response = requests.get(j_url, headers=headers)
    data = response.json()
    like_check = [] # 좋아요 수
    id_check = [] # 곡 일련번호
    contsid_data = [item for item in data['contsLike'] if 'SUMMCNT' in item]

    for i in range(len(contsid_data)):
        like_check.append(contsid_data[i]['SUMMCNT'])
        id_check.append(contsid_data[i]['CONTSID'])
    url = "https://www.melon.com/chart/index.htm"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    
    tbody_tag = soup.find("tbody")  

    img_tags = tbody_tag.find_all("img")

    url_list = [img.get("src") for img in img_tags]
    
    melon_list = []

    for i in range(100): 
        id_res = id_check[i]               
        rank_res = song_rank_list[i]
        album_res = album_list[i] 
        title_res = song_title_list[i]
        name_res = singer_list[i]
        url_res = url_list[i]
        like_res = like_check[i]
        song_info = {               # 딕셔너리 구조
                "곡일련번호": id_res,
                "순위": rank_res,
                "앨범": album_res,
                "곡명": title_res,
                "가수": name_res,
                "커버이미지_주소" : url_res,
                "좋아요" : like_res,
            }
        melon_list.append(song_info)
    result = pd.DataFrame(melon_list) # 시각화 자료 return
 
    return result

    


# In[24]:


import pandas as pd   # 결과

df = 멜론차트_가져오기()

print(df.shape)
df.head()


# In[ ]:




