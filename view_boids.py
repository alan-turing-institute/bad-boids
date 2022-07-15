"""
Display a Boids animation
"""
from matplotlib import animation
from matplotlib import pyplot as plt

from boids import Flock


def view_boids(flock, xlim=(-500, 1500), ylim=(-500, 1500), frames=50, interval=50):
    """Display an animation of a Flock of Boid

    Parameters
    ----------
    flock : Flock
        The Flock of Boid to animate
    xlim : tuple, optional
        x-axis limits for animation, by default (-500, 1500)
    ylim : tuple, optional
        y-axis limits for animation, by default (-500, 1500)
    frames : int, optional
        Number of Flock updates in the animation, by default 50
    interval : int, optional
        Time between animation frames in milliseconds, by default 50
    """
    figure = plt.figure()
    axes = plt.axes(xlim=xlim, ylim=ylim)
    scatter = axes.scatter(
        [b.position[0] for b in flock.boids], [b.position[1] for b in flock.boids]
    )

    def animate(_):
        """Update the flock and the Boid positions in the scatter plot

        Parameters
        ----------
        _ : None
             Needed for compatiblity with animation.FuncAnimation
        """
        flock.update()
        scatter.set_offsets([b.position for b in flock.boids])

    _ = animation.FuncAnimation(figure, animate, frames=frames, interval=interval)
    plt.show()


if __name__ == "__main__":
    boid_count = 50
    flock = Flock.with_default_parameters(boid_count)
    flock.initialise_random(boid_count)
    view_boids(flock)
