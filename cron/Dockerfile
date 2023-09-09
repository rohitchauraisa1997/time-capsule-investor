FROM python:3.9

WORKDIR /app

# Install cron and any other necessary packages
RUN apt-get update && apt-get install -y cron

# Create a directory for logs
RUN mkdir /var/log/cron

# Create and activate a virtual environment
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip

# Install any dependencies inside the virtual environment
RUN /app/venv/bin/pip install sqlalchemy pytz requests pymysql

# Copy your Python script into the container
COPY env.json /app/env.json
COPY nasdaq_stocks_cron.py /app/nasdaq_stocks_cron.py
COPY nse_stocks_cron.py /app/nse_stocks_cron.py
COPY utils.py /app/utils.py
COPY test.py /app/test.py

RUN echo "10 * * * * root cd /app; /app/venv/bin/python /app/test.py >> /var/log/cron/crontest.log 2>&1" > /etc/cron.d/my-cron-job-test
# Update database every 2 hours with latest price..
RUN echo "0 */2 * * * root cd /app; /app/venv/bin/python /app/nasdaq_stocks_cron.py >> /var/log/cron/cronnasdaq.log 2>&1" > /etc/cron.d/my-cron-job-nasdaq
RUN echo "0 */2 * * * root cd /app; /app/venv/bin/python /app/nse_stocks_cron.py >> /var/log/cron/cronnse.log 2>&1" > /etc/cron.d/my-cron-job-nse

# Give execution permission to the cron job file
RUN chmod 0644 /etc/cron.d/my-cron-job-test
RUN chmod 0644 /etc/cron.d/my-cron-job-nasdaq
RUN chmod 0644 /etc/cron.d/my-cron-job-nse

# Start the cron service in the foreground
CMD ["cron", "-f"]
