# MLOPTIFLOW

Dynamic MLOps Framework with Integrated CLI for Automated ML Project Inception, Kafka-Driven Real-Time Model Monitoring, and Adaptive Canary Deployment Architectures


## Installation

1. create a new virtual environment with python ^3.11 and activate it

2. install poetry:

```bash
pip install poetry
```

3. install mloptiflow:

```bash
pip install mloptiflow
```

4. initialize a new project and choose a name and paradigm (currently supported paradigms are: `tabular_regression`, `tabular_classification`, `demo_tabular_classification`)[demo ones are just a minimalistic examples of the paradigm]:

```bash
mloptiflow init <your-project-name> --paradigm=<paradigm-name>
```

5. `cd` into your project directory:

```bash
cd <your-project-name>
```

6. install dependencies:

```bash
poetry install
```

or if using `pip`:

```bash
pip install -r requirements.txt
```

## DEMO Test

1. create a new virtual environment with python ^3.11 and activate it

2. install poetry:

```bash
pip install poetry
```

3. install mloptiflow:

```bash
pip install mloptiflow
```

4. initialize a new project with the name `demo-project` and paradigm `demo_tabular_classification`:

```bash
mloptiflow init demo-project --paradigm=demo_tabular_classification
```

5. `cd` into your project directory:

```bash
cd demo-project
```

6. install dependencies:

```bash
poetry install
```

7. run the training pipeline:

```bash
mloptiflow train start
```

8. run and test the inference API:

```bash
mloptiflow deploy start --with-api-test
```

## Usage
- TBA

## Support
- TBA

## Roadmap
- TBA

## Contributing
- TBA


## License
MIT
