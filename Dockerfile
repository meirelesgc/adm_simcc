FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi

EXPOSE 5002

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5002", "adm_simcc:create_app", "--reload", "--log-level", "error", "--access-logfile", "-", "--error-logfile", "-", "--workers", "4"]
