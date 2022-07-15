"""
Display a Boids animation
"""
import argparse

from matplotlib import animation  # type: ignore
from matplotlib import pyplot as plt  # type: ignore

from boids import Flock


def view_boids(
    flock: Flock,
    xlim: tuple[float, float] = (-500, 1500),
    ylim: tuple[float, float] = (-500, 1500),
    frames: int = 50,
    interval: int = 50,
):
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


def main():
    parser = argparse.ArgumentParser(description="Display a boids simulation")
    parser.add_argument("boid_count", help="How many boids to simulate", type=int)
    args = parser.parse_args()
    flock = Flock.with_default_parameters(args.boid_count)
    flock.initialise_random(args.boid_count)
    view_boids(flock)
