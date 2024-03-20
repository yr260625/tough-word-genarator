import csv
import time

from bs4 import BeautifulSoup
import requests

from batch.tough_word_collector.animan_board import AnimanBoard


class MainUsecase:
    """docstring for ClassName."""

    def __init__(self):
        """コンストラクタ"""
        pass

    def collect_board_responses_per_page(self, page):
        board_url_list = self.__get_board_url_list_per_page(page)
        for board_url in board_url_list:
            board = AnimanBoard(board_url)
            csv_data = self.__create_csv_data(board)
            self.__output_csv(csv_data)
            self.__output_collected(board.get_id())
            time.sleep(5)
        pass

    def __get_board_url_list_per_page(self, page) -> list[AnimanBoard]:
        # カテゴリ『TOUGH(タフ)』
        category_url = f"https://bbs.animanch.com/kakolog27/page:{page}"
        print(f"start request for {category_url}")
        category_res = requests.get(category_url, timeout=10)
        category_res.raise_for_status()
        category_soup = BeautifulSoup(category_res.text, "html.parser")

        # 掲示板URL一覧(レスが固定された過去ログから取得する)
        board_link_list = category_soup.select("#mainThread a")
        board_url_list = []
        for board_link in board_link_list:
            url = board_link.get("href")
            if not self.__has_collected(url):
                board_url_list.append(url)
        return board_url_list

    def __create_csv_data(self, animan_board: AnimanBoard):
        # CSV出力データ作成
        id = animan_board.get_id()
        title = animan_board.get_title()
        output_list = []
        for res in animan_board.get_res_list():
            line = [id, title, "\n".join(res)]
            output_list.append(line)
        return output_list

    def __output_csv(self, output_list):
        # csv出力
        with open("static/tough_board.csv", "a", encoding="utf_8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(output_list)

    def __output_collected(self, url):
        # csv出力
        with open("static/tough_collected.csv", "a", encoding="utf_8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow([url])

    def __has_collected(self, url):
        """収集済みかどうか

        Returns:
            bool: 収集済みかどうか
        """
        with open("static/tough_collected.csv", mode="r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            # 指定した文字列を含む行を取得
            for line in lines:
                if url == f"https://bbs.animanch.com/board/{line}/":
                    return True
        return False