FROM python:3.8.10-slim

WORKDIR /tests

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest"]