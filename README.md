
## Stage 2 — Dependency Data Collection

### Description

The application retrieves package metadata from a Python package
repository using its HTTP API.

It extracts and displays direct dependencies of the specified
Python package.

### Implementation

- Uses the PyPI JSON API.
- Uses only the Python standard library.
- Retrieves metadata with urllib.
- Parses JSON using json.
- Extracts dependencies from info.requires_dist.
- Handles HTTP, connection and JSON errors.
- Does not install packages or use package managers.

### Run

```cmd
run.bat --package flask --repo https://pypi.org/pypi/flask/json
```

### Run tests

```cmd
py -m unittest discover -s tests -v
```

### Demo

```cmd
scripts\demo_stage2.bat
```

### Project status

- Stage 1: completed.
- Stage 2: completed.
