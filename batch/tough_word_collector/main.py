import csv
import os
import time
from batch.tough_word_collector.animan_board_scraper import AnimanBoardScraper
from batch.tough_word_collector.animan_page_scraper import AnimanPageScraper


def collect_board_url_list(start: int, end: int) -> list[str]:
    """過去ログのページから掲示板URLを収集

        Args:
        start (int): 開始ページNo.
        end (int): 終了ページNo.

    Returns:
        list[str]: 掲示板URL一覧
    """
    target_board_url_list = []
    for page in range(start, end + 1):
        page_scraper = AnimanPageScraper.create(page)
        target_board_url_list += page_scraper.get_board_url_list()
        time.sleep(2)
    return target_board_url_list


def collect_board_responses(board_url_list: list[str]):
    """与えられたURLの掲示板をスクレイピング

    Args:
        board_url_list (list[str]): 掲示板URL一覧
    """
    for board_url in board_url_list:
        if not has_collected(board_url):
            board = AnimanBoardScraper.create(board_url)
            to_csv(board)
            append_to_collected_csv(board)
            time.sleep(2)
    pass


def to_csv(board: AnimanBoardScraper):
    """CSV出力

    Args:
        board (AnimanBoardScraper): 掲示板
    """
    with open("static/tough_board.csv", "a", encoding="utf_8") as f:
        csv_data = board.create_csv_data()
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(csv_data)


def append_to_collected_csv(board: AnimanBoardScraper):
    """出力済みCSVに追記

    Args:
        board (AnimanBoardScraper): 掲示板
    """
    with open("static/tough_collected.csv", "a", encoding="utf_8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([board.get_id()])


def has_collected(url: str):
    """収集済みかどうか

    Args:
        url (str): 掲示板URL

    Returns:
        bool: 収集済みかどうか
    """
    with open("static/tough_collected.csv", mode="r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        # 指定した文字列を含む行を取得
        for line in lines:
            if url == f"{os.environ['ANIMAN_BORAD_URL']}{line}/":
                return True
    return False


if __name__ == "__main__":

    try:
        url_list = collect_board_url_list(1, 2)
        collect_board_responses(url_list)
    except Exception as e:
        print(e)
        raise e
