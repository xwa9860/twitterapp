#!/bin/bash
gunicorn run:app --daemon
python worker.py
