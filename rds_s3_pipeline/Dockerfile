FROM python:latest

WORKDIR /pipeline

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY errors.py .
COPY daily_extract.py .

CMD python3 daily_extract.py