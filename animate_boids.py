from matplotlib import pyplot as plt
from matplotlib import animation
from boids import updateBoids, initialize_boids

boids = initialize_boids()
figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids[0], boids[1])


def ANIMATE(frame):
    updateBoids(boids)
    scatter.set_offsets(list(zip(boids[0], boids[1])))


anim = animation.FuncAnimation(figure, ANIMATE, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
