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


def boid_interaction(
    me,
    other,
    count,
    flock_attraction,
    avoidance_radius,
    formation_flying_radius,
    speed_matching_strength,
):
    my_x, my_y, my_xv, my_yv = me
    their_x, their_y, their_xv, their_yv = other

    x_separation = their_x - my_x
    y_separation = their_y - my_y

    delta_xv = 0
    delta_yv = 0
    # Fly towards the middle
    delta_xv += x_separation * flock_attraction / count
    delta_yv += y_separation * flock_attraction / count
    # Fly away from nearby boids
    separation_sq = x_separation ** 2 + y_separation ** 2
    if separation_sq < avoidance_radius ** 2:
        delta_xv -= x_separation
        delta_yv -= y_separation
    # Try to match speed with nearby boids
    if separation_sq < formation_flying_radius ** 2:
        delta_xv += (their_xv - my_xv) * speed_matching_strength / count
        delta_yv += (their_yv - my_yv) * speed_matching_strength / count

    return delta_xv, delta_yv


def update_boids(
    boids,
    flock_attraction=0.01,
    avoidance_radius=10,
    formation_flying_radius=100,
    speed_matching_strength=0.125,
):
    xs, ys, xvs, yvs = boids

    # Compute boid velocity updates
    delta_xvs = [0] * len(xs)
    delta_yvs = [0] * len(xs)
    for i in range(len(xs)):
        me = (xs[i], ys[i], xvs[i], yvs[i])
        for j in range(len(xs)):
            other = (xs[j], ys[j], xvs[j], yvs[j])
            dxv, dyv = boid_interaction(
                me,
                other,
                len(xs),
                flock_attraction,
                avoidance_radius,
                formation_flying_radius,
                speed_matching_strength,
            )
            delta_xvs[i] += dxv
            delta_yvs[i] += dyv

    # Apply updates
    for i in range(len(xs)):
        # Update velocities
        xvs[i] += delta_xvs[i]
        yvs[i] += delta_yvs[i]
        # Move according to velocities
        xs[i] += xvs[i]
        ys[i] += yvs[i]


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
