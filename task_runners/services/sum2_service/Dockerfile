FROM python:3.9

EXPOSE 5000

WORKDIR /service

COPY * /service
COPY ../common /common
RUN pip install -r requirements.txt
RUN pip install -r ../common/requirements.txt

CMD python3 sum2_controller.py