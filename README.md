# emoji-data

[![CI](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/emoji-data/badge/?version=latest)](https://emoji-data.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/emoji-data.svg)](https://pypi.org/project/emoji-data/)

A library that represents emoji sequences and characters based on the [Unicode® Technical Standard #51 Data Files](https://unicode.org/reports/tr51/#emoji_data).

## Install

```sh
pip install emoji-data
```

## How to use

See [`docs/notebooks/example.ipynb`](docs/notebooks/example.ipynb)

## Development

### Updating emoji data files

To update the emoji data files from Unicode:

```bash
python scripts/download.py
```

This script uses `httpx` with concurrent downloads and displays progress bars. Files are saved to `src/emoji_data/data/`.
