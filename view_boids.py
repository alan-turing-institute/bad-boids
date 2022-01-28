from matplotlib import pyplot as plt
from matplotlib import animation
from boids import Boids

boid_count = 50
boids = Boids.with_default_parameters(boid_count)
boids.initialise_random(boid_count)
figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter([b.x for b in boids.boids], [b.y for b in boids.boids])


def animate(frame):
    boids.update()
    scatter.set_offsets([(b.x, b.y) for b in boids.boids])


anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
