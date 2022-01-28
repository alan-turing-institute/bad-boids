import os
import yaml
from pytest import approx
from boids import Boids


def test_bad_boids_regression():
    with open(os.path.join(os.path.dirname(__file__), "fixture.yml")) as fixture_file:
        regression_data = yaml.safe_load(fixture_file)
    boid_count = 50
    boids = Boids.with_default_parameters(boid_count)
    boids.initialise_from_data(regression_data["before"])
    boids.update()
    current_data = (boids.xs, boids.ys, boids.xvs, boids.yvs)
    for after, before in zip(regression_data["after"], current_data):
        for after_value, before_value in zip(after, before):
            assert after_value == approx(before_value)


def test_bad_boids_initialisation():
    boid_count = 15
    boids = Boids.with_default_parameters(boid_count)
    x_range = (-450, 50.0)
    y_range = (300.0, 600.0)
    xv_range = (0, 10.0)
    yv_range = (-20.0, 20.0)
    boids.initialise_random(
        boid_count,
        x_range=x_range,
        y_range=y_range,
        xv_range=xv_range,
        yv_range=yv_range,
    )
    assert len(boids.xs) == boid_count
    for x in boids.xs:
        assert x < x_range[1]
        assert x > x_range[0]
    for y in boids.ys:
        assert y < y_range[1]
        assert y > y_range[0]
    for xv in boids.xvs:
        assert xv < xv_range[1]
        assert xv > xv_range[0]
    for yv in boids.yvs:
        assert yv < yv_range[1]
        assert yv > yv_range[0]
