FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
RUN mkdir /home/bluetreasure
COPY . /home/bluetreasure/
RUN pip install --no-cache-dir -r /home/bluetreasure/requirements.txt
WORKDIR /home/bluetreasure
CMD ["uwsgi", "--ini", "uwsgi.ini"]
