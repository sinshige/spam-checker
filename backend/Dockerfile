FROM python:3.12-slim

WORKDIR /app

# 開発に必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリの定義ファイルをコピー
COPY requirements.txt .

# FastAPI, Uvicorn, Ruff, Pytestなどをコンテナ内にインストール
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]