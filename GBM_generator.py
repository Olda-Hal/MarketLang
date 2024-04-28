import numpy as np
import random


class GBM_generator:
    def __init__(self):
        self.generator = self.simulate_gbm()
        next(self.generator)

    def simulate_gbm(n=1000, dt=0.008, x0=100, sigma_step=0.03, sigma_max=0.05):
        """
        Simulates the Geometric Brownian Motion (GBM) process.

        Args:
            n (int): The number of time steps in the simulation. Default is 1000.
            dt (float): The time increment between each step. Default is 0.008.
            x0 (float): The initial value of the process. Default is 100.
            sigma_step (float): The step size for the sigma parameter. Default is 0.03.
            sigma_max (float): The maximum value of the sigma parameter. Default is 0.05.

        Returns:
            float: The last value of each simulation.
        """

        sigma = np.arange(sigma_step, sigma_max, sigma_step)

        x = x0
        mu = yield  # initial value of mu
        while True:
            dx = (mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size=len(sigma))
            x = x * np.exp(dx)
            mu = yield x[-1]  # yield the last value of each simulation and receive the next mu
