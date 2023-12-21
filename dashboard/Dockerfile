FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY database.py .
COPY utilities.py .
COPY visualisations.py .
COPY app.py .

CMD streamlit run app.py