FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libdbus-1-dev \
    libglib2.0-dev \
    pkg-config \
    cmake \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /cybertea_project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

#RUN python manage.py collectstatic

EXPOSE 8000
CMD ["python3", "manage.py", "runserver"]