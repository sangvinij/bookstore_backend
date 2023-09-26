#!/bin/bash
alembic upgrade head
python create_superuser.py
uvicorn project.main:app --host 0.0.0.0 --port 8000
