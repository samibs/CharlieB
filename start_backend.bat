@echo off
set PYTHONPATH=app
uvicorn app.backend.main:app --reload