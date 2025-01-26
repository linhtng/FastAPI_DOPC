FROM python:3.10

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app /code/app/
COPY tests tests
COPY locustfile.py locustfile.py
COPY run_load_test.sh run_load_test.sh

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "app.main:app", "--reload"]