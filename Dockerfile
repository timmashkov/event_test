FROM python:3.12

WORKDIR /event_project


COPY requirements.txt /event_project/
RUN pip install --upgrade pip; pip install  -r /event_project/requirements.txt

COPY . .
