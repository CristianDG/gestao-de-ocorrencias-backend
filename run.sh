!/usr/bin/env

source "./.env"
flask $@ -e .env --app src/app.py  run --port $PORT
