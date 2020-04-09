from matplotlib import pyplot as plt
import numpy as np

cmap = plt.get_cmap('jet_r')
LIM = 1
NUM_CHAIR_PARTS = 3
# CHAIR_SCALE = 0.4
CHAIR_SCALE = 1

NUM_SAMPLES_PER_PART = 1000

cube_lines = [(5, 7), (3, 7), (1, 3), (1, 5),
                (0, 1), (4, 5), (2, 3), (6, 7),
                (0, 4), (0, 2), (2, 6), (4, 6)]

# of surfaces
cube_surfaces = [
    (0, 2, 3, 1),
    (1, 3, 7, 5),
    (4, 6, 7, 5),
    (0, 2, 6, 4),
    (1, 0, 4, 5),
    (2, 6, 7, 3)
]

SCALE = 0.5

identity = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 0]])