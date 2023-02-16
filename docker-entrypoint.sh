#!/usr/bin/env bash

echo "migrate db"
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

