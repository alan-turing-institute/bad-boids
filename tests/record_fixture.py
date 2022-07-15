import yaml

from boids import Boid, Flock


def boids_to_coords(
    boids: list[Boid],
) -> tuple[list[float], list[float], list[float], list[float]]:
    """Convert a list of Boid into lists of coordinates

    Parameters
    ----------
    boids : list
        List of Boid instances

    Returns
    -------
    tuple
        Length 4 tuple containing lists of x, y, xv and yv coordinates for each Boid
    """
    # Convert to standard Python floats below as yaml.dump raises RepresenterError
    # with numpy floats.
    return (
        [float(boid.position[0]) for boid in boids],  # x
        [float(boid.position[1]) for boid in boids],  # y
        [float(boid.velocity[0]) for boid in boids],  # xv
        [float(boid.velocity[1]) for boid in boids],  # yv
    )


def record_fixture(boid_count: int = 50, random_seed: int = 123):
    """Save a yaml of Boid coordinates before and after an update to use in a
    regression test.

    Parameters
    ----------
    boid_count : int, optional
        Number of Boid, by default 50
    random_seed : int, optional
        Random seed for generating initial Boid coordinates, by default 123
    """
    flock = Flock.with_default_parameters(boid_count)
    flock.initialise_random(boid_count, random_seed=random_seed)
    before = boids_to_coords(flock.boids)
    flock.update()
    after = boids_to_coords(flock.boids)
    fixture = {"before": before, "after": after}
    with open("fixture.yml", "w") as fixture_file:
        fixture_file.write(yaml.safe_dump(fixture))


if __name__ == "__main__":
    record_fixture()
