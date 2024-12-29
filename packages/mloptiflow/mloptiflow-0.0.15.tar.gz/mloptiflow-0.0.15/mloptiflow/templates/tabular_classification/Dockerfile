FROM python:3.11-slim

WORKDIR /{{ project_name }}

RUN apt-get update && apt-get install -y \
    build-essential curl software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install

EXPOSE 8501

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
