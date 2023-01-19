#!/usr/bin/env sh

source "./.env"
flask $@ -e .env --app src/main.py run --port $PORT
