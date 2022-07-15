# better_boids

An improved implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.

To see the original version before refactoring see the [main branch](https://github.com/jack89roberts/bad-boids/tree/main).

Adapted from:

- https://github.com/UCL/bad-boids
- https://github.com/jamespjh/bad-boids

## Setup

Clone the repo, then install the requirements (from the `bad-boids` directory):

```bash
pip install -r requirements.txt
```

Tested on Python 3.9. We recommend installing the requirements in a virtual environment of your choice.

## Usage

To view a Boids animation run (from the `bad-boids` directory):

```bash
python view_boids.py
```

## Development

### Code quality checks

We use `black`, `isort` and `flake8` to check the code style, and `mypy` for type checking. To run all checks run the following from the `bad-boids` directory:

```bash
isort .
black .
flake8
mypy .
```

Alternatively, we have provided a [pre-commit](https://pre-commit.com/) config that will run all these automatically when making git commits. To install the hooks run:

```bash
pre-commit install --install-hooks
```

Then to manually run all checks on all files run:

```bash
pre-commit run -a
```

### Testing

We use `pytest`, to run all tests simply run 

```bash
pytest
```

from the `bad-boids` directory.
