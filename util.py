import numpy as np
import matplotlib.pyplot as plt

class NoiseGenerator:

    def __init__(self, order=0, max_change=0, initial_values=[], allow_negatives=True) -> None:
        self.order = order
        self.max_change = max_change
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
        self.noise_values[-1] = 2 * self.max_change * np.random.random() - self.max_change
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

def create_price_generator(initial_value, volatility):
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
    noise_gen = create_price_generator(11000, 10)

    xs = range(24 * 30 * 12)
    ys = np.array([noise_gen.tick() for _ in xs])

    plt.plot(xs, ys)
    plt.show()
