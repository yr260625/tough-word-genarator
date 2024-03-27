from pathlib import Path
from bs4 import BeautifulSoup
from batch.tough_word_collector.animan_page_scraper import AnimanPageScraper
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
    with open(f"{get_project_root()}/data/test_page.html", "r", encoding="utf-8") as f:
        response = f.read()

    return MockResponse(response, 200)


def test_get_board_url_list(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    scraper = AnimanPageScraper.create(1)
    board_url_list = scraper.get_board_url_list()
    assert type(board_url_list) is list
    assert len(board_url_list) == 100
    assert board_url_list[0] == "https://bbs.animanch.com/board/3137500/"
    assert board_url_list[99] == "https://bbs.animanch.com/board/3136565/"
