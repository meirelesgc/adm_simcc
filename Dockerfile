FROM python:3.9-slim



ENV POETRY_VIRTUALENVS_CREATE=false \
    ADM_DATABASE=$ADM_DATABASE \
    ADM_USER=$ADM_USER \
    ADM_HOST=$ADM_HOST \
    ADM_PASSWORD=$ADM_PASSWORD \
    ADM_PORT=$ADM_PORT

WORKDIR /app

COPY . .

RUN pip install poetry && \
    poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-ansi && \
    apt-get update && apt-get clean

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "app:app"]
