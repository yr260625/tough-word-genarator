from janome.tokenizer import Tokenizer
import re
import numpy as np
import pandas as pd
import markovify
import pickle
import os

# 使用ファイル一覧
INPUT_FILE = "static/tough_board.csv"
TEMP_FILE = "static/tough_word_splitted.txt"
OUTPUT_FILE = "static/tough_word_model.pkl"

# 掲示板タイトル列番号
BOARD_TITLE_COL = 1
# 掲示板レス列番号
BOARD_RES_COL = 2


def preprocess():
    """前処理"""
    # ファイルの読み込み
    res_data = pd.read_csv(INPUT_FILE, header=None, usecols=[BOARD_RES_COL])
    res_list = np.array(res_data)

    t = Tokenizer()
    with open(TEMP_FILE, "w", encoding="utf-8") as output:
        for sentence in res_list:
            # 不要文字削除
            result = __sanitize(sentence)
            # 分かち書き
            tokens = list(t.tokenize(result, wakati=True))
            splitted_text = " ".join([str(token) for token in tokens])
            # 出力
            output.write(f"{splitted_text}\n")


def create_model():
    """マルコフ連鎖モデル作成"""

    # runtime error防止
    # ref: https://github.com/SamuraiT/mecab-python3/issues/54
    CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
    CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'

    # モデル生成
    with open(TEMP_FILE, "r", encoding="utf-8") as input:
        tough_word_model = markovify.NewlineText(
            input.read(), well_formed=False, state_size=2
        )

    # 生成したモデルをpicke形式で保存
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(tough_word_model, f)


def __sanitize(sentence: str):
    """不要文字列削除

    Args:
        sentence (str): 返還前文字列

    Returns:
        str: 変換後文字列
    """
    ret = sentence
    # URL削除
    ret = re.sub(
        r"h?(ttps?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)",
        "",
        str(ret),
    )
    # "このレスは削除されています" 削除
    ret = re.sub(r"このレスは削除されています", "", str(ret))

    return ret


def postprocessing():
    """後処理"""
    if os.path.isfile(TEMP_FILE):
        os.remove(TEMP_FILE)


if __name__ == "__main__":

    try:
        preprocess()
        create_model()
        postprocessing()
    except Exception as e:
        postprocessing()
        print(e)
        raise e
