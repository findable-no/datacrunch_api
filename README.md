# Introduction

This is the API for the Datacrunch project.

It is a Python wrapper around the Datacrunch REST API.

The REST API is documented at <https://api.datacrunch.io/v1/docs#tag/serverless-containers/GET/v1/>.

# Installation

Currently, the only way to install is to clone the repository and install manually:

```bash
pip install -e .
```

# Implementation details

The API is implemented as a Python wrapper around the Datacrunch REST API.

The wrapper is generated using the `requests` library and Cursor.

pyproject.toml contains the dependencies.

Install dependencies with `pip install -e .[dev]`

