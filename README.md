# Better boids
Refactoring exercise of the Research Software Engineering Course of the Allan Turing Institute. Original version before refactoring is [here](https://github.com/jack89roberts/bad-boids/tree/main).
## Setup

Clone the repo, then install the requirements (from the `better-boids` directory):
```
pip install -r requirements.txt
```
Tested on Python 3.9. We recommend installing the requirements in a virtual environment of your choice.

## Usage

To view a Boids animation run (from the `better-boids` directory):

```
python animate_boids.py
```

## Development

We use `black` and `flake8` to check the code style, and `pytest` for testing. To lint and test the code run (from the `better-boids` directory):

```
black .
flake8
pytest
```

