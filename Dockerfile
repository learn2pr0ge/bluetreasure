FROM python:3.11-slim
WORKDIR /home/bluetreasure
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
RUN mkdir /home/bluetreasure
COPY requirements.txt .
RUN pip install --no-cache-dir -r /home/bluetreasure/requirements.txt
COPY . /home/bluetreasure/
CMD ["uwsgi", "--ini", "uwsgi.ini"]
