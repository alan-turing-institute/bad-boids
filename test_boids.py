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
    boid_count = 50
    x_range = (-450, 50.0)
    y_range = (300.0, 600.0)
    xv_range = (0, 10.0)
    yv_range = (-20.0, 20.0)
    xs, ys, xvs, yvs = initialise_boids(
        boid_count,
        x_range=x_range,
        y_range=y_range,
        xv_range=xv_range,
        yv_range=yv_range,
    )
    assert len(xs) == boid_count
    for x in xs:
        assert x < x_range[1]
        assert x > x_range[0]
    for y in ys:
        assert y < y_range[1]
        assert y > y_range[0]
    for xv in xvs:
        assert xv < xv_range[1]
        assert xv > xv_range[0]
    for yv in yvs:
        assert yv < yv_range[1]
        assert yv > yv_range[0]
