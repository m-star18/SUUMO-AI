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
        self.result = requests.get(URL)
        self.content = self.result.content
        self.soup = BeautifulSoup(self.content)

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
