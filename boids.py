"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
import numpy as np
import random


class Boid:
    def __init__(self, x, y, vx, vy, owner):
        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])
        self.owner = owner

    def interact(self, other):
        """Compute velocity changes due to one other boid"""

        delta_v = np.array([0.0, 0.0])
        separation = other.position - self.position
        separation_square = separation.dot(separation)

        # Fly towards the middle
        delta_v += separation * self.owner.parameters["flock_attraction"]

        # Fly away from nearby boids
        if separation_square < self.owener.parameters["avoidance_radius"] ** 2:
            delta_v -= separation

        # Try to match speed with nearby boids
        if separation_square < self.owner.parameters["formation_flying_radius"] ** 2:
            delta_v += (other.velocity - self.velocity) * self.owner.parameters[
                "speed_matching_strength"
            ]
        return delta_v

    def move(self, delta_v):
        """Update the position and velocity of the Boid"""
        self.velocity += delta_v
        self.position += self.velocity


class Flock:
    def __init__(self, parameters):
        self.parameters = parameters
        self.boids = []

    def __len__(self):
        return len(self.boids)

    # Ownership of Boids
    # Adjust velocity: match speed, fly to center, fly away from others
    # Init flock


# Deliberately terrible code for teaching purposes
def initialize_boids(
    boid_count,
    x_range=(-450, 50.0),
    y_range=(300.0, 600.0),
    xv_range=(0, 10.0),
    yv_range=(-20.0, 20.0),
):
    boids_x = [random.uniform(*x_range) for x in range(boid_count)]
    boids_y = [random.uniform(*y_range) for x in range(boid_count)]
    boid_x_velocities = [random.uniform(*xv_range) for x in range(boid_count)]
    boid_y_velocities = [random.uniform(*yv_range) for x in range(boid_count)]
    return (boids_x, boids_y, boid_x_velocities, boid_y_velocities)


def updateBoids(boids):
    xs, ys, xvs, yvs = boids
    deltaXVs = [0] * len(xs)
    deltaYVs = [0] * len(xs)
    # Fly towards the middle
    for i in range(len(xs)):
        for j in range(len(xs)):
            deltaXVs[i] = deltaXVs[i] + (xs[j] - xs[i]) * 0.01 / len(xs)
    for i in range(len(xs)):
        for j in range(len(xs)):
            deltaYVs[i] = deltaYVs[i] + (ys[j] - ys[i]) * 0.01 / len(xs)
    # Fly away from nearby boids
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 < 100:
                deltaXVs[i] = deltaXVs[i] + (xs[i] - xs[j])
                deltaYVs[i] = deltaYVs[i] + (ys[i] - ys[j])
    # Try to match speed with nearby boids
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 < 10000:
                deltaXVs[i] = deltaXVs[i] + (xvs[j] - xvs[i]) * 0.125 / len(xs)
                deltaYVs[i] = deltaYVs[i] + (yvs[j] - yvs[i]) * 0.125 / len(xs)
    # Update velocities
    for i in range(len(xs)):
        xvs[i] = xvs[i] + deltaXVs[i]
        yvs[i] = yvs[i] + deltaYVs[i]
    # Move according to velocities
    for i in range(len(xs)):
        xs[i] = xs[i] + xvs[i]
        ys[i] = ys[i] + yvs[i]
