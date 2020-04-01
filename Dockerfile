FROM python:3.6

RUN echo "Asia/Shanghai" > /etc/timezone \
 && rm /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install wheel \
 && pip install -r /app/requirements.txt \
 && rm -rf ~/.cache/pip \
 && apt update && apt install -y cron && service cron start


COPY . /app/
COPY ./crontab.txt /var/spool/cron/root

