FROM python:3.9-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
COPY .env /app/


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENTRYPOINT ["/bin/bash"]