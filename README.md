# タフ語録生成ツール

## 概要

本ツールによって、以下のことを実行する。
* カテゴリ『TOUGH(タフ)』のあにまん掲示板のレスを抽出
* 分かち書きした抽出結果を元に、マルコフ連鎖のモデルを作成
* モデルからタフ語録のような文章を生成

## How to use

1. 依存関係をインストール:

   ```bash
   pip install -r requirements.txt
   ```

2. レス収集

   ```bash
   python -m batch.tough_word_collector
   ```

3. モデル作成

   ```bash
   python -m batch.tough_word_splitter
   ```

4. サーバーを起動してAPI実行

   ```bash
   uvicorn app.main:app --reload
   ```

## 参考メモ

### pytestについて

* requests.getをモック
  * https://zenn.dev/re24_1986/articles/0a7895b1429bfa
  * 具体的なレスポンスをシミュレーターファイルでモック
  * pytest-mockを使う

## Todo

### 別の仕組みを用いて語録生成

今回は単純に実装したかったため、マルコフ連鎖を選択したが、今後はその他の仕組みを用いた文章生成を行うことも検討する。

  * RNN、CNN
  * LLMのファインチューニング
  * word2Vec

### 語録風文章への変換

最終的には、入力値を語録風の言い回しに変換できるようにしたい。
