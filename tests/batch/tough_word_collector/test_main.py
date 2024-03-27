import os
import batch.tough_word_collector.main as main
from batch.tough_word_collector.animan_page_scraper import AnimanPageScraper


def mocked_create(page):
    class MockPageScraper:
        def __init__(self, page: int):
            self.page = page
            self.url = f'{os.environ["ANIMAN_TOUGH_CATEGORY_URL"]}page:{page}'
            print(f"start request for {self.url}")

        def get_board_url_list(self):
            return ["url1", "url2"]

    return MockPageScraper(page)


def mocked_sleep(second):
    print(f"sleep {second} second")
    pass


def test_collect_board_url_list(mocker):

    # AnimanPageScraper.createをモック化
    mocker.patch(
        "batch.tough_word_collector.animan_page_scraper.AnimanPageScraper.create",
        side_effect=lambda x: mocked_create(x),
    )
    # sleepをモック化
    mocker.patch("time.sleep", side_effect=mocked_sleep)

    result = main.collect_board_url_list(1, 5)
    assert type(result) is list
    assert type(result[0]) is str
    assert len(result) == 10
