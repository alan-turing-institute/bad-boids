import os
import yaml
from pytest import approx
from boids import initialise_boids, update_boids


def test_bad_boids_regression():
    with open(os.path.join(os.path.dirname(__file__), "fixture.yml")) as fixture_file:
        regression_data = yaml.safe_load(fixture_file)

    boid_data = regression_data["before"]
    update_boids(boid_data)
    for after, before in zip(regression_data["after"], boid_data):
        for after_value, before_value in zip(after, before):
            assert after_value == approx(before_value)


def test_bad_boids_initialisation():
    xs, ys, xvs, yvs = initialise_boids()
    assert len(xs) == 50
    for x in xs:
        assert x < 50.0
        assert x > -450
    for y in ys:
        assert y < 600
        assert y > 300
    for xv in xvs:
        assert xv < 10.0
        assert xv > 0
    for yv in yvs:
        assert yv < 20.0
        assert yv > -20.0
