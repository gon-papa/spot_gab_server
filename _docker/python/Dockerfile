# ベースイメージの選択
FROM python:3.9

SHELL ["/bin/bash", "-c"]

# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルのコピー
COPY ./pyproject.toml /app/pyproject.toml

# Poetryのインストールと設定
RUN curl -sSL https://install.python-poetry.org | python - && \
    echo "export PATH=\$PATH:/root/.local/bin" >> ~/.bashrc && \
    . ~/.bashrc && \
    poetry config virtualenvs.create false && \
    poetry install

RUN apt-get update && \
    apt-get install -y sqlite3

# アプリケーションのコードをコピー
COPY . /app

# アプリケーションの起動コマンドを設定
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
