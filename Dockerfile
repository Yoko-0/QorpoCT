# Dockerfile
FROM python:3.11

WORKDIR /QorpoCT

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "QorpoApp.main:app"]