#!/bin/bash

cd /fea-app
gunicorn -w 2 -k uvicorn.workers.UvicornH11Worker api.main:fea_app --bind 0.0.0.0:5900
