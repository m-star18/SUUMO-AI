import time

from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame

from const import URL


class SuumoScrapyJob:
    def __init__(self):
        """
        Attributes
        ----------
        """
        self.result = requests.get(URL)
        self.content = self.result.content
        self.soup = BeautifulSoup(self.content)

        self.name = []  # マンション名
        self.address = []  # 住所
        self.locations0 = []  # 立地1つ目（最寄駅/徒歩~分）
        self.locations1 = []  # 立地2つ目（最寄駅/徒歩~分）
        self.locations2 = []  # 立地3つ目（最寄駅/徒歩~分）
        self.age = []  # 築年数
        self.height = []  # 建物高さ
        self.floor = []  # 階
        self.rent = []  # 賃料
        self.admin = []  # 管理費
        self.deposit = []  # 敷金
        self.others = []  # 礼金
        self.floor_plan = []  # 間取り
        self.area = []  # 専有面積
