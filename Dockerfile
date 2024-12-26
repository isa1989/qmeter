# Python 3.11 Slim imajını kullan
FROM python:3.11-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini oluştur
WORKDIR /app

# Gereksinim dosyasını kopyala
COPY requirements.txt .

# Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uygulamanın başlatılacağı komut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "qmeter.wsgi:application"]
