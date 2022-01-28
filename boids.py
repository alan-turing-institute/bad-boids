"""
A deliberately bad implementation of Boids[1] for use as an exercise on refactoring.

[1] http://dl.acm.org/citation.cfm?doid=37401.37406
"""
import random

# Deliberately terrible code for teaching purposes


class Boid:
    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv


class Boids:
    def __init__(self, parameters):
        self.parameters = parameters

    @classmethod
    def with_default_parameters(cls, boid_count):
        parameters = {
            "flock_attraction": 0.01 / boid_count,
            "avoidance_radius": 10,
            "formation_flying_radius": 100,
            "speed_matching_strength": 0.125 / boid_count,
        }
        return cls(parameters)

    def initialise_random(
        self,
        boid_count,
        x_range=(-450, 50.0),
        y_range=(300.0, 600.0),
        xv_range=(0, 10.0),
        yv_range=(-20.0, 20.0),
    ):
        self.boids = [
            Boid(
                random.uniform(*x_range),
                random.uniform(*y_range),
                random.uniform(*xv_range),
                random.uniform(*yv_range),
            )
            for _ in range(boid_count)
        ]

    def initialise_from_data(self, data):
        self.boids = [Boid(x, y, xv, yv) for x, y, xv, yv in zip(*data)]

    def boid_interaction(self, me, other):
        x_separation = other.x - me.x
        y_separation = other.y - me.y

        delta_xv = 0
        delta_yv = 0
        # Fly towards the middle
        delta_xv += x_separation * self.parameters["flock_attraction"]
        delta_yv += y_separation * self.parameters["flock_attraction"]
        # Fly away from nearby boids
        separation_sq = x_separation ** 2 + y_separation ** 2
        if separation_sq < self.parameters["avoidance_radius"] ** 2:
            delta_xv -= x_separation
            delta_yv -= y_separation
        # Try to match speed with nearby boids
        if separation_sq < self.parameters["formation_flying_radius"] ** 2:
            delta_xv += (other.xv - me.xv) * self.parameters["speed_matching_strength"]
            delta_yv += (other.yv - me.yv) * self.parameters["speed_matching_strength"]

        return delta_xv, delta_yv

    def update(self):
        # Compute boid velocity updates
        delta_xvs = [0] * len(self.boids)
        delta_yvs = [0] * len(self.boids)
        for i, me in enumerate(self.boids):
            for other in self.boids:
                dxv, dyv = self.boid_interaction(me, other)
                delta_xvs[i] += dxv
                delta_yvs[i] += dyv

        # Apply updates
        for i, me in enumerate(self.boids):
            # Update velocities
            me.xv += delta_xvs[i]
            me.yv += delta_yvs[i]
            # Move according to velocities
            me.x += me.xv
            me.y += me.yv
