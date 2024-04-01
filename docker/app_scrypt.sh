#!/usr/bin/bash

alembic upgrade head

cd src/

uvicorn runner:start_app --host 0.0.0.0 --port 8000 --reload
