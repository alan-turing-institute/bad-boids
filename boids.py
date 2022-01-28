"""
A deliberately bad implementation of Boids[1] for use as an exercise on refactoring.

[1] http://dl.acm.org/citation.cfm?doid=37401.37406
"""
import random

# Deliberately terrible code for teaching purposes


class Boid:
    def __init__(self, x, y, xv, yv, owner):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.owner = owner

    def interaction(self, other):
        delta_xv = 0
        delta_yv = 0
        x_separation = other.x - self.x
        y_separation = other.y - self.y
        separation_sq = x_separation ** 2 + y_separation ** 2

        # Fly towards the middle
        flock_atraction = self.owner.parameters["flock_attraction"]
        delta_xv += x_separation * flock_atraction
        delta_yv += y_separation * flock_atraction

        # Fly away from nearby boids
        avoidance_radius = self.owner.parameters["avoidance_radius"]
        if separation_sq < avoidance_radius ** 2:
            delta_xv -= x_separation
            delta_yv -= y_separation

        # Try to match speed with nearby boids
        formation_flying_radius = self.owner.parameters["formation_flying_radius"]
        speed_matching_strength = self.owner.parameters["speed_matching_strength"]
        if separation_sq < formation_flying_radius ** 2:
            delta_xv += (other.xv - self.xv) * speed_matching_strength
            delta_yv += (other.yv - self.yv) * speed_matching_strength

        return delta_xv, delta_yv


class Boids:
    def __init__(self, parameters):
        self.parameters = parameters
        self.boids = []

    @classmethod
    def with_default_parameters(cls, boid_count):
        parameters = {
            "flock_attraction": 0.01 / boid_count,
            "avoidance_radius": 10,
            "formation_flying_radius": 100,
            "speed_matching_strength": 0.125 / boid_count,
        }
        return cls(parameters)

    @property
    def boid_count(self):
        return len(self.boids)

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
                self,
            )
            for _ in range(boid_count)
        ]

    def initialise_from_data(self, data):
        self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]

    def update(self):
        # Compute boid velocity updates
        delta_xvs = [0] * self.boid_count
        delta_yvs = [0] * self.boid_count
        for i, me in enumerate(self.boids):
            for other in self.boids:
                dxv, dyv = me.interaction(other)
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
