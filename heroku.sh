#!/bin/bash
gunicorn app:app
# gunicorn app:app --daemon
# python worker.py
