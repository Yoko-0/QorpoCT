# Dockerfile
FROM python:3.11

RUN mkdir /QorpoCT
WORKDIR /QorpoCT
ADD . /QorpoCT/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "QorpoApp.main:app"]