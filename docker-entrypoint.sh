#!/usr/bin/env bash

echo "migrate db"
./manage.py migrate
./manage.py runserver 8000

