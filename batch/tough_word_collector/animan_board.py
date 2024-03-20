import requests
import datetime
import re
from bs4 import BeautifulSoup


class AnimanBoard:

    def __init__(self, url):
        """コンストラクタ

        Args:
            url: あにまん掲示板のURL
        """
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self) -> BeautifulSoup:
        """HTMLパーサー

        Returns:
            BeautifulSoup: _description_
        """
        print(f"start request for {self.url}")
        res = requests.get(self.url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # brタグを改行に変換
        delimiter = "\n"
        for line_break in soup.select("br"):
            line_break.replaceWith(delimiter)

        # レスアンカーを削除
        for line_break in soup.select(".reslink"):
            line_break.extract()

        return soup

    def get_id(self) -> str:
        """掲示板ID取得

        Returns:
            str: 掲示板ID
        """
        return re.sub("https://bbs.animanch.com/board/|/", "", self.url)

    def get_title(self) -> str:
        """掲示板タイトル取得

        Returns:
            str: 掲示板タイトル
        """
        title_tag = self.soup.select_one("#threadTitle")
        if title_tag is not None:
            return title_tag.get_text()
        return "No Title"
        

    def get_created_date(self):
        """掲示板作成日時取得

        Returns:
            datetime: 掲示板作成日時
        """
        date_tag = self.soup.select_one("#res1 .resposted")
        if date_tag is None:
            return "No Date"
        date_str = date_tag.get_text()
        data_str_extract_weekday = re.sub("\\(.+\\)", "", date_str)
        return datetime.datetime.strptime(data_str_extract_weekday, "%y/%m/%d %H:%M:%S")

    def get_res_list(self):
        """全レス取得

        Returns:
            list[list[str]]: 全レス
        """
        res_list = []
        res_body_list = self.soup.select(".list-group-item .resbody")
        for res_body in res_body_list:
            res_sentence_list = []
            for p_list in res_body.select("p"):
                text_list = p_list.get_text().split("br")
                for text in text_list:
                    if text != "":
                        res_sentence_list.append(text)
            res_list.append(res_sentence_list)
        return res_list