from matplotlib import pyplot as plt
from matplotlib import animation
from boids import Flock


def view_boids(flock, xlim=(-500, 1500), ylim=(-500, 1500), frames=50, interval=50):
    figure = plt.figure()
    axes = plt.axes(xlim=xlim, ylim=ylim)
    scatter = axes.scatter(
        [b.position[0] for b in flock.boids], [b.position[1] for b in flock.boids]
    )

    def animate(_):
        flock.update()
        scatter.set_offsets([b.position for b in flock.boids])

    _ = animation.FuncAnimation(figure, animate, frames=frames, interval=interval)
    plt.show()


if __name__ == "__main__":
    boid_count = 50
    flock = Flock.with_default_parameters(boid_count)
    flock.initialize_random(boid_count)
    view_boids(flock)
