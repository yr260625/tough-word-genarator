import csv
import os
import time

from bs4 import BeautifulSoup
import requests

from batch.tough_word_collector.animan_board_scraper import AnimanBoardScraper


class AnimanPageScraper:
    """docstring for ClassName."""

    def __init__(self, page: int):
        """コンストラクタ"""
        self.page = page
        self.url = f'{os.environ["ANIMAN_TOUGH_CATEGORY_URL"]}page:{page}'

    @classmethod
    def create(cls, page: int):
        """ファクトリーメソッド

        Args:
            page (int): _description_

        Returns:
            _type_: _description_
        """
        instance = cls(page)
        instance.set_soup()
        return instance

    def set_soup(self):
        """HTMLパーサー"""
        print(f"start request for {self.url}")
        res = requests.get(self.url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        self.soup = soup

    def get_board_url_list(self) -> list[str]:
        # 掲示板URL一覧(レスが固定された過去ログから取得する)
        board_link_list = self.soup.select("#mainThread a")
        board_url_list = []
        for board_link in board_link_list:
            url = board_link.get("href")
            if url is not None:
                board_url_list.append(url)
        return board_url_list
