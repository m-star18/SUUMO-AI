import time

from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame


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
