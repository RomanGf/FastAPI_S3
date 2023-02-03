FROM python:3.10-slim

COPY . .

WORKDIR /

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload", "--port", "8000" ]