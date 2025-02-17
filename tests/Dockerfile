FROM python:3.9

RUN pip install pytest

COPY ./tests /tests

WORKDIR /tests

CMD ["pytest"]