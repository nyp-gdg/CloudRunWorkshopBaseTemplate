FROM python:3.11-slim

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY app/wsgi.py ./wsgi.py

ENV PORT=8080
CMD ["gunicorn", "--bind", ":8080", "wsgi:app"]