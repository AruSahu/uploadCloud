#!/bin/bash
cd /home/ubuntu/cloud_hw
sudo /home/ubuntu/web_tier/venv/bin/gunicorn \
    --bind 0.0.0.0:80 \
    --workers 2 \
    --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --log-level warning \
    --access-logfile - \
    --error-logfile - \
    wsgi:app
