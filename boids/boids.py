"""
An improved implementation of Boids[1] for use as an exercise on refactoring.

[1] http://dl.acm.org/citation.cfm?doid=37401.37406
"""
import random
from typing import Union

import numpy as np
import numpy.typing as npt


class Boid:
    """
    A single Boid that has an owner (a Flock)

    Attributes
    ----------
    position : np.ndarray
        Length 2 array storing the Boid's x and y position
    velocity : np.ndarray
        Length 2 array storing the Boid's x and y velocity
    owner : Flock
        The Flock this Boid belongs to

    Methods
    -------
    interaction(other)
        Compute the forces on this Boid due to one other Boid.

    move(delta_v)
        Increment the Boid's velocity and position.
    """

    def __init__(self, x: float, y: float, xv: float, yv: float, owner: "Flock"):
        """Create a single Boid.

        Parameters
        ----------
        x : float
            Initial x position
        y : float
            Initial y position
        xv : float
            Initial x velocity
        yv : float
            Initial y velocity
        owner : Flock
            The Flock this Boid belongs to
        """
        self.position: npt.NDArray[np.float64] = np.array([x, y])
        self.velocity: npt.NDArray[np.float64] = np.array([xv, yv])
        self.owner = owner

    def interaction(self, other: "Boid") -> npt.NDArray[np.float64]:
        """Compute the forces on this Boid due to one other Boid.

        Parameters
        ----------
        other : Boid
            Another Boid

        Returns
        -------
        np.ndarray
            Velocity change caused by the other Boid
        """
        delta_v = np.array([0.0, 0.0])
        separation = other.position - self.position
        separation_sq = separation.dot(separation)

        # Fly towards the middle
        flock_attraction = self.owner.parameters["flock_attraction"]
        delta_v += separation * flock_attraction

        # Fly away from nearby boids
        avoidance_radius = self.owner.parameters["avoidance_radius"]
        if separation_sq < avoidance_radius**2:
            delta_v -= separation

        # Try to match speed with nearby boids
        formation_flying_radius = self.owner.parameters["formation_flying_radius"]
        speed_matching_strength = self.owner.parameters["speed_matching_strength"]
        if separation_sq < formation_flying_radius**2:
            delta_v += (other.velocity - self.velocity) * speed_matching_strength

        return delta_v

    def move(self, delta_v: npt.NDArray[np.float64]):
        """Update the position and velocity of the Boid

        Parameters
        ----------
        delta_v : np.ndarray
            Amount to update the x and y velocity
        """
        self.velocity += delta_v
        self.position += self.velocity


class Flock:
    """
    A flock of Boid governed by a set of interaction parameters.

    Attributes
    ----------
    parameters : dict
        Parameters controlling the flock behaviour, with keys 'flock_attraction',
        'avoidance_radius', 'formation_flying_radius', and 'speed_matching_strength'
    boids : list
        List of Boid in this Flock

    boid_count : int
        The number of Boid currently in the Flock

    Methods
    -------
    with_default_parameters(boid_count)
        Create a Flock instance with default parameters for a given number of Boid.

    initialise_random(boid_count, x_range, y_range, xv_range, yv_range)
        Generate a number of Boid with random initial positions and velocities.

    initialise_from_data(data)
        Generate Boid from input data.

    update()
        Update the position and velocity of all the Boid
    """

    def __init__(self, parameters: dict[str, float]):
        """Create an empty Flock (with parameters but no Boid).

        Parameters
        ----------
        parameters : dict
            Parameters controlling the flock behaviour. Must include the keys
            'flock_attraction', 'avoidance_radius', 'formation_flying_radius',
            and 'speed_matching_strength'
        """
        self.parameters = parameters
        self.boids: list[Boid] = []

    @classmethod
    def with_default_parameters(cls, boid_count: int) -> "Flock":
        """Create an empty Flock with default parameters for a given flock size

        Parameters
        ----------
        boid_count : int
            Compute parameters for a Flock with this many Boid.

        Returns
        -------
        Flock
            An empty Flock (with no Boid)
        """
        parameters = {
            "flock_attraction": 0.01 / boid_count,
            "avoidance_radius": 10,
            "formation_flying_radius": 100,
            "speed_matching_strength": 0.125 / boid_count,
        }
        return cls(parameters)

    @property
    def boid_count(self) -> int:
        """Get the number of Boids currently in this Flock.

        Returns
        -------
        int
            Number of Boid currently in this Flock.
        """
        return len(self.boids)

    def initialise_random(
        self,
        boid_count: int,
        x_range: tuple[float, float] = (-450, 50.0),
        y_range: tuple[float, float] = (300.0, 600.0),
        xv_range: tuple[float, float] = (0, 10.0),
        yv_range: tuple[float, float] = (-20.0, 20.0),
        random_seed: Union[int, float, str, bytes, bytearray] = None,
    ):
        """Set self.boids to a number of Boid with random positions.

        Parameters
        ----------
        boid_count : int
            The number of Boid to generate.
        x_range : tuple, optional
            Min and max x position, by default (-450, 50.0)
        y_range : tuple, optional
            Min and max y position, by default (300.0, 600.0)
        xv_range : tuple, optional
            Min and max x velocity, by default (0, 10.0)
        yv_range : tuple, optional
            Min and max y velocity, by default (-20.0, 20.0)
        random_seed : int, float, str, bytes, or bytearray, optional
            Random seed passed to random.Random()
        """
        rng = random.Random(random_seed)
        self.boids = [
            Boid(
                rng.uniform(*x_range),
                rng.uniform(*y_range),
                rng.uniform(*xv_range),
                rng.uniform(*yv_range),
                self,
            )
            for _ in range(boid_count)
        ]

    def initialise_from_data(self, data: list[list[float]]):
        """Use input data to set self.boids.

        Parameters
        ----------
        data : list
            List of length 4 with positions and velocities for each Boid to create
            (in [x, y, xv, yv] order)
        """
        self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]

    def update(self):
        """Update the velocities and positions of all the Boid in this Flock"""
        # Compute boid velocity updates
        delta_vs = np.zeros((self.boid_count, 2))
        for i, me in enumerate(self.boids):
            for other in self.boids:
                delta_vs[i, :] += me.interaction(other)

        # Apply updates
        for i, me in enumerate(self.boids):
            me.move(delta_vs[i, :])
