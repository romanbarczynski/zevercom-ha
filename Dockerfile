FROM python:3.7-bullseye

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY entrypoint.sh zevercom.py /

ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh"]
