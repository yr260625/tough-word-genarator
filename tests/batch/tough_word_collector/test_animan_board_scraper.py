from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from batch.tough_word_collector.animan_board_scraper import AnimanBoardScraper
from pathlib import Path


def get_project_root():
    return Path(__file__).parent


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.__text = text
            self.__status_code = status_code

        @property
        def text(self):
            return self.__text

        def raise_for_status(self):
            if self.__status_code != 200:
                raise Exception("requests error")

    response = ""
    with open(f"{get_project_root()}/data/test_board.html", "r", encoding="utf-8") as f:
        response = f.read()

    return MockResponse(response, 200)


def test_get_id(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    scraper = AnimanBoardScraper.create("https://bbs.animanch.com/board/9999999/")
    id = scraper.get_id()
    assert id == "9999999"


def test_get_title(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    scraper = AnimanBoardScraper.create("https://bbs.animanch.com/board/9999999/")
    title = scraper.get_title()
    assert title == "あにまん民が浅いジャンルって…"


def test_get_created_date(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    scraper = AnimanBoardScraper.create("https://bbs.animanch.com/board/9999999/")
    date = scraper.get_created_date()
    print(date)
    assert type(date) is datetime


def test_create_csv_data(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    scraper = AnimanBoardScraper.create("https://bbs.animanch.com/board/9999999/")
    csv_data = scraper.create_csv_data()
    print(csv_data)
    assert type(csv_data) is list
    assert type(csv_data[0]) is list
    assert type(csv_data[0][0]) is str
    assert type(csv_data[0][1]) is str
    assert type(csv_data[0][2]) is str
    assert csv_data[0] == ["9999999", "あにまん民が浅いジャンルって…", "ま…まさか"]
