FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 5000
CMD poetry run gunicorn --certfile=$CERT_FILE --keyfile=$KEY_FILE -b 0.0.0.0:5000 app:app --reload