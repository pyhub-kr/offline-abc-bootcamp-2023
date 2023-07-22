import datetime
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from .utils import percent_to_float


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
}


def get_국내증시_검색상위(field_id_list=None):
    if field_id_list is None:
        field_id_list = ["quant", "open_val", "high_val", "low_val", "per", "roe"]

    url = "https://finance.naver.com/sise/field_submit.naver"
    params = {
        "menu": "lastsearch2",
        "returnUrl": "http://finance.naver.com/sise/lastsearch2.naver",
        "fieldIds": field_id_list,
    }
    
    res = requests.get(url, params=params, headers=headers)
    html = res.text
    
    df = pd.read_html(html, header=0)[1]
    df = df.dropna().drop(['순위'], axis="columns").set_index('종목명')
    df['검색비율'] = percent_to_float(df['검색비율'])
    df['등락률'] = percent_to_float(df['등락률'])
    
    return df


def get_실시간_국내증시_인기검색종목():
    sise_url = 'https://finance.naver.com/sise/'

    res = requests.get(sise_url, headers=headers)
    res.raise_for_status()
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    
    item_list = []

    for tag in soup.select('#popularItemList li'):
        name_tag = tag.select_one('a')
        url = urljoin(sise_url, name_tag['href'])
        code = parse_qs(urlparse(url).query)['code'][0]
        name = name_tag.text.strip()
        value_tag = tag.select_one('.up, .dn, .noc')
        direction = ' '.join(value_tag['class'])
        value = int(value_tag.text.replace(',', ''))
        item_list.append({
            '종목명': name,
            '종목코드': code,
            'direction': direction,
            '거래가': value,
            'url': url,
        })

    df = pd.DataFrame(item_list).set_index('종목명')

    return df


def get_종목별_일별_거래량(code, max_page=3):
    '60일치 거래량 데이터 크롤링'

    # ref: https://finance.naver.com/item/frgn.naver?code=005930

    for page in range(1, max_page+1):  # 페이지당 20개 * 3페이지
        params = {
            'code': code,
            'page': page,
        }
        res = requests.get("https://finance.naver.com/item/frgn.naver", params=params, headers=headers)
        html = res.text

        df = pd.read_html(html)[2].dropna(how='all')
        df.columns = [
            '날짜', '종가', '전일비', '등락률', '거래량',
            '기관 - 순매매량', '외국인 - 순매매량', '외국인 - 보유주수', '외국인 - 보유율(%)',
        ]
        df = df.iloc[2:].set_index('날짜')
        df.index = pd.to_datetime(df.index)

        df['종가'] = df['종가'].astype('float')
        df['전일비'] = df['전일비'].astype('float')
        df['거래량'] = df['거래량'].astype('float')
        
        df['등락률'] = percent_to_float(df['등락률'])
        df['외국인 - 보유율(%)'] = percent_to_float(df['외국인 - 보유율(%)'])

        # 이미 float로 파싱되는 듯.
        df['기관 - 순매매량'] = df['기관 - 순매매량'].astype('str')
        df['기관 - 순매매량'] = df['기관 - 순매매량'].apply(lambda s: float(s.replace(',', '')))

        df['외국인 - 순매매량'] = df['외국인 - 순매매량'].astype('str')
        df['외국인 - 순매매량'] = df['외국인 - 순매매량'].apply(lambda s: float(s.replace(',', '')))

        yield df

        time.sleep(0.1)


def get_주가시장별_시간별_시세(code, max_page=100):
    url = "https://finance.naver.com/sise/sise_index_time.naver"
    return get_시간별_시세(code, url, max_page)


def get_종목별_시간별_시세(code, max_page=100):
    url = "https://finance.naver.com/item/sise_time.naver"
    return get_시간별_시세(code, url, max_page)


def get_시간별_시세(code, url, max_page=100):
    # ref: https://finance.naver.com/item/sise.naver?code=005930

    now = datetime.datetime.now()

    # TODO: 주말 시간대일 경우, 금요일 시간대로의 변경이 필요.
    # ref: https://finance.naver.com/item/sise_time.naver?code=005930&thistime=20230721161127
    if 5 <= now.weekday() <= 6:  # Monday == 0 ... Sunday == 6.
        # Calculate the number of days to subtract from the current date to get the most recent Friday
        days_to_subtract = (now.weekday() - 4) % 7
        now = now.replace(hour=16, minute=0, second=0, microsecond=0) - datetime.timedelta(days=days_to_subtract)

    if now.hour < 9:
        now = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(seconds=1)

    thistime = now.strftime('%Y%m%d%H%M00')  

    df_list = []
    last_df = None

    for page in range(1, max_page+1):
        params = {
            "code": code,
            "thistime": thistime,
            "page": page,
        }

        res = requests.get(url, params=params, headers=headers)
        html = res.text
        page_df = pd.read_html(html, header=0)[0].dropna()

        def apply_fn(t):
            hour, minute = map(int, t.split(':'))
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        page_df['체결시각'] = page_df['체결시각'].apply(apply_fn)
        page_df = page_df.set_index('체결시각')

        if last_df is not None:
            is_over_page = last_df.index.equals(page_df.index)
            if is_over_page:
                break

        last_df = page_df

        df_list.append(page_df)
        if page_df.empty:
            break

    return pd.concat(df_list)


def get_kospi200(code, max_page=1):
    last_df = None

    for page in range(1, max_page+1):
        params = {
            'code': code,
            'page': page,
        }
        res = requests.get("https://finance.naver.com/sise/sise_index_day.naver", params=params, headers=headers)
        res.raise_for_status()
        html = res.text

        current_df = pd.read_html(html, header=0)[0]
        current_df = current_df.dropna().set_index('날짜')
        current_df.index = pd.to_datetime(current_df.index)

        if last_df is not None:
            is_over_page = last_df.index.equals(current_df.index)
            if is_over_page:
                break

        last_df = current_df

        yield current_df

        time.sleep(0.1)
