from copy import deepcopy
import yaml
import boids

before = deepcopy(boids.boids)
boids.updateBoids(boids.boids)
after = boids.boids
fixture = {"before": before, "after": after}
with open("fixture.yml", "w") as fixture_file:
    fixture_file.write(yaml.safe_dump(fixture))
