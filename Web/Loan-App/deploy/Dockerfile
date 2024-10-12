FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app", "--worker-class", "gevent"]
