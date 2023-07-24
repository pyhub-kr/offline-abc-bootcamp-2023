#!/usr/bin/env python
# coding: utf-8

# In[110]:


index_page_url = "https://m.comic.naver.com/webtoon/list?titleId=793275&page=1"


# In[111]:


import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin


# In[112]:


res = requests.get (index_page_url)
res


# In[113]:


html = res.text


# In[114]:


soup = BeautifulSoup(html, "html.parser")
soup


# In[115]:


tag_list = soup.select(".section_episode_list a")


# In[116]:


for a_tag in tag_list: # 교수님이 알려주신 코드
    ep_url = a_tag ["href"]
    if ep_url != "#":
        # 태그는 다시 . select를 통해 자식 태그들을 조회할 수 있습니다.
        name_tag = a_tag.select(".name")[0]
        name = name_tag.text
        print (name)
        print (ep_url)
        # ep_url에서는 scheme과 서버 hostnameol 누락되어있습니다.
        # html 요청 주소를 보시면 https://m.comic.naver.com 입니다.
        # 이 값을 하드코딩으로 적용하셔도 되구요.
        ep_url = "https://m.comic.naver.com" + ep_url
        # 아래 코드처럼 동적으로 hostname을 조합하실 수 있습니다.
        ep_url = urljoin(index_page_url, ep_url)
        print(ep_url)


# In[118]:


import os
import requests
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin

webtoon_name = "작전명순정"
os.makedirs(webtoon_name, exist_ok=True)

for idx, a_tag in tqdm(enumerate(tag_list, start=1)):
    ep_url = a_tag["href"]
    if ep_url != "#":
        # 태그는 다시 .select를 통해 자식 태그들을 조회할 수 있습니다.
        name_tag = a_tag.select(".name")[0]
        name = name_tag.text
        print(name)
        print(ep_url)

        # 이미지 URL을 완전한 주소로 만들어줍니다.
        base_url = "https://m.comic.naver.com"
        ep_url = urljoin(base_url, ep_url)

        print(ep_url)  # Check if the episode URL is correct

        episode_folder = f"{webtoon_name}/{idx:02d}화"
        os.makedirs(episode_folder, exist_ok=True)

        # 해당 URL로 접근하여 페이지를 가져옵니다.
        response = requests.get(ep_url)
        if response.status_code != 200:
            print(f"Error: {ep_url}에 접근하는데 문제가 발생했습니다.")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # 이미지 URL을 추출하여 다운로드합니다.
        image_tags = soup.select(".comic img")
        for image_tag in image_tags:
            image_url = image_tag["src"]  # 이미지 URL을 추출합니다.

            print(image_url)  # Check if the image URL is correct

            image_res = requests.get(image_url, headers=headers)
            if image_res.status_code != 200:
                print(f"Error: {image_url} 이미지 다운로드에 실패했습니다.")
                continue

            # 이미지 파일명을 추출합니다.
            image_filename = f"{idx:03d}.jpg"

            # 이미지 파일의 절대 경로를 구성합니다.
            filepath = os.path.join(episode_folder, image_filename)

            # 이미지 다운로드 및 저장
            with open(filepath, "wb") as f:
                f.write(image_res.content)

            print(f"{filepath} 저장 완료")

