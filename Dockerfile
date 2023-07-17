FROM python:3.8-slim-buster

WORKDIR /root

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    cron

COPY crawling.py .
COPY cron /etc/cron.d/cron
COPY requirements.txt .

RUN pip install -r requirements.txt

# Give execution access
RUN chmod 0755 /etc/cron.d/cron
# Run cron job on cron file
RUN crontab /etc/cron.d/cron
# Create the log file
RUN touch /var/log/cron.log

CMD ["cron", "-f"]