FROM python:latest

WORKDIR /code
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD .env .
ADD main.py .
CMD ["python", "./main.py"]
