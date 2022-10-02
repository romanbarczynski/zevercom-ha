FROM python:3.7-bullseye

RUN pip install paho-mqtt requests

COPY entrypoint.sh zevercom.py /

ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh"]
