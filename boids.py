"""
A deliberately bad implementation of Boids[1] for use as an exercise on refactoring.

[1] http://dl.acm.org/citation.cfm?doid=37401.37406
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random

# Deliberately terrible code for teaching purposes


def initialise_boids(
    boid_count,
    x_range=(-450, 50.0),
    y_range=(300.0, 600.0),
    xv_range=(0, 10.0),
    yv_range=(-20.0, 20.0),
):
    boids_x = [random.uniform(*x_range) for _ in range(boid_count)]
    boids_y = [random.uniform(*y_range) for _ in range(boid_count)]
    boid_x_velocities = [random.uniform(*xv_range) for _ in range(boid_count)]
    boid_y_velocities = [random.uniform(*yv_range) for _ in range(boid_count)]
    return (boids_x, boids_y, boid_x_velocities, boid_y_velocities)


def update_boids(boids):
    xs, ys, xvs, yvs = boids

    # Compute boid velocity updates
    delta_xvs = [0] * len(xs)
    delta_yvs = [0] * len(xs)
    for i in range(len(xs)):
        for j in range(len(xs)):
            # Fly towards the middle
            delta_xvs[i] = delta_xvs[i] + (xs[j] - xs[i]) * 0.01 / len(xs)
            delta_yvs[i] = delta_yvs[i] + (ys[j] - ys[i]) * 0.01 / len(xs)
            # Fly away from nearby boids
            if (xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 < 100:
                delta_xvs[i] = delta_xvs[i] + (xs[i] - xs[j])
                delta_yvs[i] = delta_yvs[i] + (ys[i] - ys[j])
            # Try to match speed with nearby boids
            if (xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 < 10000:
                delta_xvs[i] = delta_xvs[i] + (xvs[j] - xvs[i]) * 0.125 / len(xs)
                delta_yvs[i] = delta_yvs[i] + (yvs[j] - yvs[i]) * 0.125 / len(xs)

    # Apply updates
    for i in range(len(xs)):
        # Update velocities
        xvs[i] = xvs[i] + delta_xvs[i]
        yvs[i] = yvs[i] + delta_yvs[i]
        # Move according to velocities
        xs[i] = xs[i] + xvs[i]
        ys[i] = ys[i] + yvs[i]


boids = initialise_boids(50)
figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids[0], boids[1])


def animate(frame):
    update_boids(boids)
    scatter.set_offsets(list(zip(boids[0], boids[1])))


anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
