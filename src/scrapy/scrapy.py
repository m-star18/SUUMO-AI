import time

from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame

from const import (
    NAME,
    FLOOR,
    RENT,
    ADMIN,
    DEPOSIT,
    OTHERS,
    FLOOR_PLAN,
    AREA,
)


def get_property_list(url):
    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content)
    summary = soup.find("div", {'id': 'js-bukkenList'})

    return soup, summary


def get_page_number(soup):
    body = soup.find("body")
    pages = body.find_all("div", {'class': 'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    pages_split0 = pages_split[0]
    pages_split1 = pages_split0[-3:]
    pages_split2 = int(pages_split1.replace('>', ''))

    return pages_split2


def get_apartment(item):
    title = item.find_all("div", {'class': 'cassetteitem_content-title'})
    title = str(title)
    title_rep = title.replace('[<div class="cassetteitem_content-title">', '')
    title_rep2 = title_rep.replace('</div>]', '')

    return title_rep2


def get_address(item):
    address = item.find_all("li", {'class': 'cassetteitem_detail-col1'})
    address = str(address)
    address_rep = address.replace('[<li class="cassetteitem_detail-col1">', '')
    address_rep2 = address_rep.replace('</li>]', '').strip()

    return address_rep2


def get_table(summary):
    tables = summary.find_all('table')

    # 各建物に対して, 売りに出ている部屋を取得
    rows = [table.find_all('tr') for table in tables]

    # 各部屋に対して, tableに入っているtext情報を格納
    data = []
    for row in rows:
        for tr in row:
            cols = tr.find_all('td') + tr.find_all('li')
            for td in cols:
                text = td.find(text=True)
                data.append(text)

    return data


class SuumoScrapyJob:
    def __init__(self, url):
        """
        Parameters
        ----------
        url: str
            スクレイピングしたいurl名.

        Attributes
        ----------
        self.name: list of str
            マンション名.
        self.address: list of str
            住所.
        self.locations0: list of str
            立地1つ目（最寄駅/徒歩~分.
        self.locations1: list of str
            立地2つ目（最寄駅/徒歩~分）.
        self.locations2: list of str
            立地3つ目（最寄駅/徒歩~分）.
        self.age: list of int
            築年数.
        self.height: list of int
            建物高さ.
        self.floor. list of int
            階.
        self.rent: list of int
            賃料.
        self.admin: list of int
            管理費.
        self.deposit: list of int
            敷金.
        self.others: list of int
            礼金.
        self.floor_plan: list of str
            間取り.
        self.area: list of int
            専有面積.
        """
        self.urls = [url]
        soup, _ = get_property_list(url)

        # ページ数の取得
        self.pages_split3 = get_page_number(soup)

        # 2ページ目から最後のページまでを格納
        for i in range(self.pages_split3 - 2):
            pg = str(i + 2)
            url_page = url + '&pn=' + pg
            self.urls.append(url_page)

        self.name = []
        self.address = []
        self.locations0 = []
        self.locations1 = []
        self.locations2 = []
        self.age = []
        self.height = []
        self.floor = []
        self.rent = []
        self.admin = []
        self.deposit = []
        self.others = []
        self.floor_plan = []
        self.area = []

        self.run()
        self.get_series()
        self.get_csv()

    def run(self):
        for i, url in enumerate(self.urls):
            print(f'{i}/{self.pages_split3}')
            # 物件リストを切り出し
            soup, summary = get_property_list(url)

            # マンション名、住所、立地（最寄駅/徒歩~分）、築年数、建物高さが入っているcassetteitemを全て抜き出し
            cassetteitems = summary.find_all("div", {'class': 'cassetteitem'})

            for item in cassetteitems:
                # 各建物から売りに出ている部屋数を取得
                tbody = item.find_all('tbody')

                # マンション名取得
                apartment = get_apartment(item)

                # 住所取得
                address = get_address(item)

                # 部屋数だけ, マンション名と住所を格納（部屋情報と数を合致させるため）
                for _ in range(len(tbody)):
                    self.name.append(apartment)
                    self.address.append(address)

                # 立地を取得
                locations = item.find_all("li", {'class': 'cassetteitem_detail-col2'})

                # 立地は、1つ目から3つ目までを取得（4つ目以降は無視）
                for location in locations:
                    cols = location.find_all('div')
                    for j, col in enumerate(cols):
                        text = col.find(text=True)
                        for _ in range(len(tbody)):
                            if j == 0:
                                self.locations0.append(text)
                            elif j == 1:
                                self.locations1.append(text)
                            elif j == 2:
                                self.locations2.append(text)

                # 築年数と建物高さを格納
                col3 = item.find_all("li", {'class': 'cassetteitem_detail-col3'})
                for x in col3:
                    cols = x.find_all('div')
                    for j, col in enumerate(cols):
                        text = col.find(text=True)
                        for y in range(len(tbody)):
                            if i == 0:
                                self.age.append(text)
                            else:
                                self.height.append(text)

                # 階、賃料、敷, 礼, 間取り、専有面積を格納
                data = get_table(summary)
                for j, flag in enumerate(data):
                    if '階' in flag:
                        self.floor.append(data[j + FLOOR])
                        self.rent.append(data[j + RENT])
                        self.admin.append(data[j + ADMIN])
                        self.deposit.append(data[j + DEPOSIT])
                        self.others.append(data[j + OTHERS])
                        self.floor_plan.append(data[j + FLOOR_PLAN])
                        self.area.append(data[j + AREA])

            time.sleep(10)

    def get_series(self):
        self.name = Series(self.name)
        self.address = Series(self.address)
        self.locations0 = Series(self.locations0)
        self.locations1 = Series(self.locations1)
        self.locations2 = Series(self.locations2)
        self.age = Series(self.age)
        self.height = Series(self.height)
        self.floor = Series(self.floor)
        self.rent = Series(self.rent)
        self.admin = Series(self.admin)
        self.deposit = Series(self.deposit)
        self.others = Series(self.others)
        self.floor_plan = Series(self.floor_plan)
        self.area = Series(self.area)

    def get_csv(self):
        # 各シリーズをデータフレーム化
        suumo_df = pd.concat([self.name, self.address, self.locations0, self.locations1, self.locations2, self.age,
                              self.height, self.floor, self.rent, self.admin, self.deposit, self.others,
                              self.floor_plan, self.area], axis=1)

        # カラム名
        suumo_df.columns = ['マンション名', '住所', '立地1', '立地2', '立地3', '築年数', '建物高さ', '階', '賃料', '管理費', '敷金',
                            '礼金', '間取り', '専有面積']

        # csvファイルとして保存
        suumo_df.to_csv(f'suumo_{NAME}.csv', sep='\t', encoding='utf-16')
