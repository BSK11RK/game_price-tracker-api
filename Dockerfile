FROM python:3.13-slim

# 作業ディレクトリ
WORKDIR /app

# requirementsコピー
COPY requirements.txt .

# install
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトコピー
COPY . .

# ポート
EXPOSE 8000

# 起動
CMD ["python", "main.py"]