import numpy as np
import random

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
    np.random.seed(1)

    sigma = np.arange(sigma_step, sigma_max, sigma_step)

    x = x0
    mu = yield  # initial value of mu
    while True:
        dx = (mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size=len(sigma))
        x = x * np.exp(dx)
        mu = yield x[-1]  # yield the last value of each simulation and receive the next mu

# usage
gbm_generator = simulate_gbm()
next(gbm_generator)  # start the generator


# generate 10 graphs with 1000 points 
# after that shows all ten graphs in one plot

import matplotlib.pyplot as plt

n = 500

plt.figure(figsize=(10, 6))


for i in range(10):
    gbm_generator = simulate_gbm()
    next(gbm_generator)
    x = np.array([gbm_generator.send(random.uniform(-3.1, 3)) for _ in range(n)])
    plt.plot(x, label=f"Simulation {i+1}")

plt.show()

# the value that is sent to the generator should be a number between -10 and 10. this value should be determined based on the buy/sell practices of the user.
