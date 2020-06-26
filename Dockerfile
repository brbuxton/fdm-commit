FROM python:3.6.10-buster

WORKDIR /app

RUN apt-get update && apt install -y git
RUN git clone https://github.com/brbuxton/fdm-commit
RUN pip install -r /app/fdm-commit/requirements.txt
ENTRYPOINT python /app/fdm-commit/fdmcommit.py