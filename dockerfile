FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY core core
COPY main.py requirements.txt .

RUN pip install -r requirements.txt

# Add crontab file
COPY crontab.txt /etc/cron.d/campground-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/campground-cron

# Apply cron job
RUN crontab /etc/cron.d/campground-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

