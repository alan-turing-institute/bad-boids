"""
A deliberately bad implementation of Boids[1] for use as an exercise on refactoring.

[1] http://dl.acm.org/citation.cfm?doid=37401.37406
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random

# Deliberately terrible code for teaching purposes


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
        self.xs = [random.uniform(*x_range) for _ in range(boid_count)]
        self.ys = [random.uniform(*y_range) for _ in range(boid_count)]
        self.xvs = [random.uniform(*xv_range) for _ in range(boid_count)]
        self.yvs = [random.uniform(*yv_range) for _ in range(boid_count)]

    def initialise_from_data(self, data):
        self.xs, self.ys, self.xvs, self.yvs = data

    def boid_interaction(self, me, other):
        my_x, my_y, my_xv, my_yv = me
        their_x, their_y, their_xv, their_yv = other

        x_separation = their_x - my_x
        y_separation = their_y - my_y

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
            delta_xv += (their_xv - my_xv) * self.parameters["speed_matching_strength"]
            delta_yv += (their_yv - my_yv) * self.parameters["speed_matching_strength"]

        return delta_xv, delta_yv

    def update(self):
        # Compute boid velocity updates
        delta_xvs = [0] * len(self.xs)
        delta_yvs = [0] * len(self.xs)
        for i in range(len(self.xs)):
            me = (self.xs[i], self.ys[i], self.xvs[i], self.yvs[i])
            for j in range(len(self.xs)):
                other = (self.xs[j], self.ys[j], self.xvs[j], self.yvs[j])
                dxv, dyv = self.boid_interaction(me, other)
                delta_xvs[i] += dxv
                delta_yvs[i] += dyv

        # Apply updates
        for i in range(len(self.xs)):
            # Update velocities
            self.xvs[i] += delta_xvs[i]
            self.yvs[i] += delta_yvs[i]
            # Move according to velocities
            self.xs[i] += self.xvs[i]
            self.ys[i] += self.yvs[i]


boid_count = 50
boids = Boids.with_default_parameters(boid_count)
boids.initialise_random(boid_count)
figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids.xs, boids.ys)


def animate(frame):
    boids.update()
    scatter.set_offsets(list(zip(boids[0], boids[1])))


anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
