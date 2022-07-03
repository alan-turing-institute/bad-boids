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

    def interaction(self, other):
        """Compute velocity changes due to one other boid"""

        delta_v = np.array([0.0, 0.0])
        separation = other.position - self.position
        separation_square = separation.dot(separation)

        # Fly towards the middle
        flock_attraction = self.owner.parameters["flock_attraction"]
        delta_v += separation * flock_attraction

        # Fly away from nearby boids
        avoidance_radius = self.owner.parameters["avoidance_radius"]
        if separation_square < avoidance_radius**2:
            delta_v -= separation

        # Try to match speed with nearby boids

        formation_flying_radius = self.owner.parameters["formation_flying_radius"]
        speed_matching_strength = self.owner.parameters["speed_matching_strength"]
        if separation_square < formation_flying_radius**2:
            delta_v += (other.velocity - self.velocity) * speed_matching_strength

        return delta_v

    def move(self, delta_v):
        """Update the position and velocity of the Boid"""
        self.velocity += delta_v
        self.position += self.velocity


class Flock:
    def __init__(self, parameters):
        self.parameters = parameters
        self.boids = []

    @classmethod
    def with_default_parameters(cls, boid_count):
        parameters = {
            "flock_attraction": 0.1 / boid_count,
            "avoidance_radius": 10,
            "formation_flying_radius": 100,
            "speed_matching_strength": 0.125 / boid_count,
        }
        return cls(parameters)

    def __len__(self):
        return len(self.boids)

    @property
    def boid_count(self):
        return len(self.boids)

    def initialize_random(
        self,
        boid_count,
        x_range=(-450, 50.0),
        y_range=(300.0, 600.0),
        xv_range=(0, 10.0),
        yv_range=(-20.0, 20.0),
        random_seed=None,
    ):
        rng = random.Random(random_seed)
        self.boids = [
            Boid(
                rng.uniform(*x_range),
                rng.uniform(*y_range),
                rng.uniform(*xv_range),
                rng.uniform(*yv_range),
                self,
            )
            for _ in range(boid_count)
        ]

    def initialize_from_data(self, data):
        self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]

    def update(self):
        delta_vs = np.zeros((self.boid_count, 2))
        for i, me in enumerate(self.boids):
            for other in self.boids:
                delta_vs[i, :] += me.interaction(other)

        for i, me in enumerate(self.boids):
            me.move(delta_vs[i, :])
