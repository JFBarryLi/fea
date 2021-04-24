#!/bin/bash

cd /fea-app
gunicorn -w 4 --forwarded-allow-ips="*" -k uvicorn.workers.UvicornH11Worker api.main:fea_app --bind 0.0.0.0:80
