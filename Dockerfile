FROM python:3.9

EXPOSE 5000

WORKDIR /

COPY api /api
COPY common /common

WORKDIR api

RUN pip3 install -r requirements.txt && pip3 install -r ../common/requirements.txt

CMD python3 tasker_api.py