#!/bin/bash
gunicorn app:app --daemon
python worker.py
python run.py
