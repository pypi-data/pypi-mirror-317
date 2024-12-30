FROM python:3.11-slim

WORKDIR /{{ project_name }}

RUN apt-get update && apt-get install -y \
    build-essential curl software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install

EXPOSE 8000

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8000/health

ENTRYPOINT ["poetry", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
