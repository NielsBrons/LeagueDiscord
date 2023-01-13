FROM python:latest

RUN --mount=type=bind, source=., target=/code
WORKDIR /code

RUN pip install -r requirements.txt
CMD ["python", "./main.py"]