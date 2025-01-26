FROM python:3.10

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app /code/app/
COPY tests tests

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app", "--reload"]