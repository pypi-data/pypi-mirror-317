# APSIT MySQL

A universal MySQL development environment using Docker. This tool provides a consistent MySQL environment across different operating systems.

## Installation

```bash
pip install apsit-mysql
```

## Prerequisites

- Python 3.6 or higher
- Docker installed and running

## Usage

Start MySQL server:
```bash
apsit-mysql start
```

Stop MySQL server:
```bash
apsit-mysql stop
```

Check server status:
```bash
apsit-mysql status
```

## Features

- Cross-platform compatibility (Windows, Linux, macOS)
- Persistent data storage using Docker volumes
- Automatic container management
- Simple CLI interface

## Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install in development mode: `pip install -e .`

## Publishing to PyPI

1. Create an account on PyPI (https://pypi.org)
2. Install build tools: `pip install build twine`
3. Build the package: `python -m build`
4. Upload to PyPI: `twine upload dist/*`
