# MLOPTIFLOW

Dynamic MLOps Framework with Integrated CLI for Automated ML Project Inception, Kafka-Driven Real-Time Model Monitoring, and Adaptive Canary Deployment Architectures


## Installation

1. create a new virtual environment with python ^3.11 and activate it

2. install mloptiflow:

```bash
pip install mloptiflow
```

3. initialize a new project and choose a name and paradigm (currently supported paradigms are: `tabular_regression`, `tabular_classification`):

```bash
mloptiflow init <your-project-name> --paradigm=<paradigm-name>
```

4. `cd` into your project directory and (if using `poetry`) update `name` field in `pyproject.toml` file:

```bash
cd <your-project-name>
```

```toml
[tool.poetry]
name = "<your-project-name>"
```

5. optionally, create a root package for the project and add `__init__.py` file:

```bash
mkdir <your-project-name>
touch <your-project-name>/__init__.py
```

6. install dependencies:

```bash
poetry install --no-root
```

or (if you created root package):

```bash
poetry install
```

or if using `pip`:

```bash
pip install -r requirements.txt
```

## Usage
1. run the application:

```bash
streamlit run app.py
```

or:

```bash
poetry run streamlit run app.py
```

2. optionally, adjust `Dockerfile` to your needs if you want to run the inference application in a containerized environment:

```dockerfile
# mainly the WORKDIR
WORKDIR /<your-project-name>
```

3. build the container image:

```bash
docker build -t <your-project-name> .
```

4. run the container image:

```bash
docker run -p 8501:8501 <your-project-name>
```

## Support
- TBA

## Roadmap
- TBA

## Contributing
- TBA


## License
MIT
