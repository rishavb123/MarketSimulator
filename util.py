import numpy as np
import matplotlib.pyplot as plt

class UniversalTicker:

    def __init__(self):
        self.tick_count = 0

    def tick(self):
        self.tick_count += 1

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "instance"):
            cls.instance = UniversalTicker()
        return cls.instance

class NoiseGenerator:

    def __init__(self, order=0, max_change=0, bias=0, initial_values=[], allow_negatives=True) -> None:
        self.order = order
        self.max_change = max_change
        self.bias = bias
        self.noise_values = np.zeros((self.order + 1), dtype=np.float)
        self.initial_values = initial_values
        self.allow_negatives = allow_negatives
        self.set_initial_values()

    def set_initial_values(self):
        for i, initial_value in enumerate(self.initial_values):
            self.noise_values[i] = initial_value

    def get_value(self):
        return self.noise_values[0]
    
    def tick(self):
        self.noise_values[-1] = 2 * self.max_change * np.random.random() - self.max_change + self.bias
        for i in range(len(self.noise_values) - 2, -1, -1):
            self.noise_values[i] += self.noise_values[i + 1]
        if not self.allow_negatives and self.get_value() < 0:
            self.set_initial_values()
            self.noise_values[0] = 0
        return self.get_value()

class CombineNoise:

    def __init__(self, *noise_generators) -> None:
        self.noise_generators = noise_generators

    def get_value(self):
        return sum(noise_generator.get_value() for noise_generator in self.noise_generators)

    def tick(self):
        return sum(noise_generator.tick() for noise_generator in self.noise_generators)

def create_price_generator(initial_value, volatility, bias=0):
    """Creates a price generator with 0th, first, and second order noise. The bias is applied in the 
    in the first order noise. A bias of 1 corresponds to around a 1.5 times increase over a 24 * 30 * 12
    tick time span (around a year if each tick is an hour).

    Args:
        initial_value (float): The initial price.
        volatility (float): The volatility of the price.
        bias (int, optional): The bias in the first order noise. Defaults to 0.

    Returns:
        CombineNoise: A noise generator that combines 0th, first, and second order noise using the parameters.
    """
    return CombineNoise(
        NoiseGenerator(
            order=0,
            max_change=5 * volatility / 100,
            initial_values=[],
            allow_negatives=True,
        ),
        NoiseGenerator(
            order=1,
            max_change=10 * volatility / 100,
            bias=bias / 150,
            initial_values=[],
            allow_negatives=True,
        ),
        NoiseGenerator(
            order=2,
            max_change=0.005 * volatility / 100,
            initial_values=[initial_value],
            allow_negatives=True,
        ),
    )

if __name__ == "__main__":

    num_runs = 100
    num_ticks = 24 * 30 * 12

    xs = range(num_ticks)
    sum_ys = np.zeros((num_ticks, ))

    for i in range(num_runs):
        noise_gen = create_price_generator(100, 10, bias=1)
        ys = np.array([noise_gen.tick() for _ in xs])

        sum_ys += ys

        plt.plot(xs, ys, c="black")

    average_run = sum_ys / num_runs

    print(average_run[-1] / average_run[0])

    plt.plot(xs, average_run, label="Average Run", c="red")

    plt.legend()

    plt.show()
