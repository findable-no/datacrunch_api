# DataCrunch API Python Client

A Python client library for interacting with the DataCrunch.io API. This library provides a clean interface for managing:

- Container deployments
- Serverless compute resources 
- Secrets
- Environment variables

## Installation

Currently, the only way to install is to clone the repository and install manually:

```bash
pip install -e .
```

# Implementation details

The API is implemented as a Python wrapper around the Datacrunch REST API.

The wrapper is generated using the `requests` library and Cursor.

pyproject.toml contains the dependencies.

Install dependencies for development with `pip install -e .[dev]`

