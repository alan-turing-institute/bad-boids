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
    for index, boid in enumerate(boids.boids):
        assert boid.x == approx(regression_data["after"][0][index])
        assert boid.y == approx(regression_data["after"][1][index])
        assert boid.xv == approx(regression_data["after"][2][index])
        assert boid.yv == approx(regression_data["after"][3][index])


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

    assert len(boids.boids) == boid_count
    assert boids.boid_count == boid_count
    for boid in boids.boids:
        assert boid.x < x_range[1]
        assert boid.x > x_range[0]
        assert boid.y < y_range[1]
        assert boid.y > y_range[0]
        assert boid.xv < xv_range[1]
        assert boid.xv > xv_range[0]
        assert boid.yv < yv_range[1]
        assert boid.yv > yv_range[0]
