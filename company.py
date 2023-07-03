import numpy as np

from entity import Entity
from util import CombineNoise, NoiseGenerator, create_price_generator

class Company(Entity):

    def __init__(self, symbol, noise_generator):
        super().__init__()
        self.symbol = symbol
        if isinstance(noise_generator, (CombineNoise, NoiseGenerator)):
            self.noise_generator = noise_generator
        else:
            self.noise_generator = create_price_generator(**noise_generator)
        self.num_shares = 0

    def release_shares(self, num_shares_to_release):
        self.num_shares += num_shares_to_release
        self.update_holdings(self.symbol, num_shares_to_release)

    def get_total_value(self):
        return self.noise_generator.get_value()

    def price_per_share(self):
        assert self.num_shares > 0
        return self.get_total_value() / self.num_shares
    
    def tick(self):
        return self.noise_generator.tick()