import os
import yaml
from pytest import approx
from boids import update_boids


def test_bad_boids_regression():
    with open(os.path.join(os.path.dirname(__file__), "fixture.yml")) as fixture_file:
        regression_data = yaml.safe_load(fixture_file)

    boid_data = regression_data["before"]
    update_boids(boid_data)
    for after, before in zip(regression_data["after"], boid_data):
        for after_value, before_value in zip(after, before):
            assert after_value == approx(before_value)
