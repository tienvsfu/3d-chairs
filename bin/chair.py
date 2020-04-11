from __future__ import print_function, division

import numpy as np
import pdb
import copy

from utils import *
from constants import *
from icp import *

class Chair():
    def __init__(self):
        self.parts = [[] for _ in range(NUM_CHAIR_PARTS)]
        self.original_parts = [[] for _ in range(NUM_CHAIR_PARTS)]

    def save(self):
        self.original_parts = copy.deepcopy(self.parts)

    def get_part(self, id):
        return self.parts[id]
    
    def set_part(self, id, new_part):
        self.parts[id] = new_part

    def fit_part(self, id, new_part):
        original_part = self.original_parts[id]
        original_sample = sample_cubes(original_part, NUM_SAMPLES_PER_PART)
        new_part_sample = sample_cubes(new_part, NUM_SAMPLES_PER_PART)
        T, distances, _ = icp(new_part_sample, original_sample, tolerance=0.0000001)

        # B = apply_transform(new_part, T)
        transformed_new_part = [apply_transform(cube, identity) for cube in new_part]

        # pdb.set_trace()
        self.parts[id] = transformed_new_part