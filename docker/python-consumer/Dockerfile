FROM python:3.8.3-alpine

ENV HOME "/root"
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PYTHONPATH ${PYTHONPATH}:/app

COPY . /app

RUN apk update && apk add curl gcc musl-dev && \
    python -m pip install --upgrade pip && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/1.1.2/get-poetry.py | python
ENV PATH "${HOME}/.poetry/bin:${PATH}"

WORKDIR /app

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

USER 1001

CMD ["python", "./consumer/app.py"]
