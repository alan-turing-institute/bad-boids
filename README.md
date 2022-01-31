# better_boids

An improved implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.

To see the original version before refactoring see the [main branch](https://github.com/jack89roberts/bad-boids/tree/main).

Adapted from:
- https://github.com/UCL/bad-boids
- https://github.com/jamespjh/bad-boids

## Setup

Clone the repo, then install the requirements (from the `bad-boids` directory):
```
pip install -r requirements.txt
```
Tested on Python 3.9. We recommend installing the requirements in a virtual environment of your choice.

## Usage

To view a Boids animation run (from the `bad-boids` directory):

```
python view_boids.py
```

## Development

We use `black` and `flake8` to check the code style, and `pytest` for testing. To lint and test the code run (from the `bad-boids` directory):

```
black .
flake8
pytest
```

