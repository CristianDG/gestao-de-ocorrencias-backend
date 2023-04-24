#!/usr/bin/env sh

flask $@ -e .env --app src/app.py  run --port $PORT
