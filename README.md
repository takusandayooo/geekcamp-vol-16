# 飲みコネクト

## 開発方法

### セットアップ

仮想環境の作成と有効化、パッケージのインストールを行う。

```shell
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
```

### APIキーを `.env` ファイルに書く

プロジェクトのルートにある `.env.example` を `.env` にコピーする

```shell
cp .env.example .env
```

APIキーを入力する。

- [OpenAI API Key](https://platform.openai.com/api-keys)
- [News API Key](https://newsapi.org/)

```.env
OPENAI_API_KEY="open ai api key here"
SEARCH_API_KEY="search api here"
```

### モジュールの実行

`module/` ディレクトリにメインの機能のプログラムがある。以下のようにモジュール名（ファイル名）を指定すると実行できる。

```shell
python3 -m module.follow_up
python3 -m module.group_split
python3 -m module.recognition_main
```

### サーバーの実行

以下のコマンドでサーバーを起動できる。URLはターミナルに表示される。

```shell
flask --app app run
```

