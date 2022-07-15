# better_boids

An improved implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.

To see the original version before refactoring see the [main branch](https://github.com/jack89roberts/bad-boids/tree/main).

Adapted from:

- https://github.com/UCL/bad-boids
- https://github.com/jamespjh/bad-boids

## Setup

Requires Python 3.9+.

Clone the repo, checkout the `better_boids` branch, then install with `pip`:

```bash
git clone https://github.com/alan-turing-institute/bad-boids.git
cd bad-boids
git checkout better_boids
pip install .
```

## Usage

To view a Boids animation run:

```bash
boids 50
```

where `50` is the number of boids to simulate.

## Development

### Poetry

We use [Poetry](https://python-poetry.org/) for development and managing dependencies. After installing poetry, set up a `boids` development environment by running:

```bash
poetry install
```

from the `bad-boids` directory (checked out to the `better_boids` branch as in the setup instructions above). Then spawn a shell in the virtual environment and run commands there:

```bash
poetry shell
```

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
