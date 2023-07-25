import os
import requests
from tqdm import tqdm
# from tqdm.notebook import tqdm
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def 웹툰_회차_목록_가져오기(title_id, page=1):
    """
    지정된 title_id의 모바일 웹툰 목록에서 지정 page의 회차 목록을 리스트로 반환합니다.
    """

    # index_page_url = "https://m.comic.naver.com/webtoon/list?titleId=769209&page=1"  # 화산귀환
    # index_page_url = f"https://m.comic.naver.com/webtoon/list?titleId={title_id}&page={page}"         # 전독시

    index_page_url = "https://m.comic.naver.com/webtoon/list"
    params = {  # parameters
        "titleId": title_id,
        "page": page,
    }
    
    res = requests.get(index_page_url, params=params)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    
    ep_tag_list = soup.select("[data-title-id]")
    ep_list = []  # ADDED
    
    for ep_tag in ep_tag_list:
        ep_title_id = ep_tag["data-title-id"]
        ep_no = ep_tag["data-no"]
        ep_title = ep_tag.select_one(".title").text.strip()
        ep_url = ep_tag.select_one("a")["href"]
        if ep_url != "#":
            ep_url = urljoin(index_page_url, ep_url)
            # print(ep_title, ep_url)
            ep_list.append({
                "title": ep_title,
                "url": ep_url,
                "title_id": ep_title_id,
                "no": ep_no,
            })  # ADDED
    
    # len(ep_list)  # ADDED

    return ep_list


# url = "https://m.comic.naver.com/webtoon/detail?titleId=747269&no=163&week=wed&listSortOrder=DESC&listPage=1"

def 웹툰_특정회차_이미지_목록_가져오기(title_id, no):
    url = "https://m.comic.naver.com/webtoon/detail"
    params = {
        "titleId": title_id,
        "no": no,
        "week": "wed",
        "listSortOrder": "DESC",
        "listPage": 1,
    }
    
    res = requests.get(url, params=params)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    image_url_list = []
    
    image_tag_list = soup.select(".toon_image")
    for image_tag in image_tag_list:
        image_url = image_tag["data-src"]
        # print(image_url)
        image_url_list.append(image_url)

    return image_url_list



def 웹툰_특정회차_이미지_목록_다운받기(base_path, image_url_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # 순차적으로 하나씩 요청해서 저장 : 멀티쓰레드, 멀티프로세스 등을 활용하면 좀 더 빠른 처리가 가능하다.
    for image_url in tqdm(image_url_list):
        res = requests.get(image_url, headers=headers)
        res.raise_for_status()  # 정상아니면 예외 발생
    
        image_filename = os.path.basename(image_url)  # 파일명 문자열만 뽑아줍니다.
    
        # filepath = f"a/b/c/"
        # filepath = os.path.join("a", "b", "c")
        filepath = os.path.join(base_path, image_filename)
    
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
    
        image_data = res.content
        with open(filepath, "wb") as f:
            f.write(image_data)


def main():
    title_id = 747269  # 화산귀환

    episode_list = 웹툰_회차_목록_가져오기(title_id)
    print(len(episode_list))

    for episode in episode_list:
        image_url_list = 웹툰_특정회차_이미지_목록_가져오기(episode["title_id"], episode["no"])

        base_path = os.path.join("webtoons", str(episode["title_id"]), str(episode["no"]))
        if not os.path.exists(base_path):
            print(f'{episode["title_id"]}, no={episode["no"]} 다운받는 중 ...')
            웹툰_특정회차_이미지_목록_다운받기(base_path, image_url_list)
        else:
            print("이미 다운받은 회차입니다.")

        # break  # 구현 중이라서, 하나만 순회토록 합니다.


main()

