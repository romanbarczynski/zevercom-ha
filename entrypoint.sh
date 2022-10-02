#!/bin/bash

export PYTHONUNBUFFERED=1

if [ -z "$1" ]; then
	python -u /zevercom.py
else
	exec "$@"
fi

