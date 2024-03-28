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
 