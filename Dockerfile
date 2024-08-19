FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir -i https://mirror.sjtu.edu.cn/pypi/web/simple
COPY . .
CMD ["gunicorn", "--workers", "2", "--worker-class", "gevent", "--worker-connections", "1000", "--bind", "0.0.0.0:5000", "app:app"]