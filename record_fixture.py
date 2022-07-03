import yaml
from boids import Flock


def boids_to_coords(boids):
    return (
        [float(boid.position[0]) for boid in boids],
        [float(boid.position[1]) for boid in boids],
        [float(boid.velocity[0]) for boid in boids],
        [float(boid.velocity[1]) for boid in boids],
    )


def record_fixture():
    boid_count = 50
    random_seed = 123
    flock = Flock.with_default_parameters(boid_count)
    flock.initialize_random(boid_count, random_seed=random_seed)
    before = boids_to_coords(flock.boids)
    flock.update()
    after = boids_to_coords(flock.boids)
    fixture = {"before": before, "after": after}
    with open("fixture.yml", "w") as fixture_file:
        fixture_file.write(yaml.safe_dump(fixture))


if __name__ == "__main__":
    record_fixture()