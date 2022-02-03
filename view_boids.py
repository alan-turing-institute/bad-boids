"""
Display a Boids animation
"""
from matplotlib import pyplot as plt
from matplotlib import animation
from boids import Flock

boid_count = 50
flock = Flock.with_default_parameters(boid_count)
flock.initialise_random(boid_count)
figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(
    [b.position[0] for b in flock.boids], [b.position[1] for b in flock.boids]
)


def animate(_):  # Needs an argument to be compatible with animation.FuncAnimation
    flock.update()
    scatter.set_offsets([b.position for b in flock.boids])


anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
