import numpy as np
from skimage.filters import gaussian


def add_dot_source(data, num=1, seed=None, sigma=1, x=None, y=None, power=1):
    """
    Add a dot source to the data.
    :param data: image data
    :param num: number of dot source
    :param seed: rand seed
    :param sigma: gaussian sigma size
    :param x: dot source x position
    :param y: dot source y position
    :param power: dot source power
    :return: image data after adding dot source
    """
    mask = np.zeros(data.shape)
    if seed is not None:
        np.random.default_rng(seed=seed)
    if x is not None and y is not None:
        mask[x][y] = np.random.random()
    else:
        shape = data.shape
        for _ in range(num):
            x = np.random.randint(0, shape[0])
            y = np.random.randint(0, shape[1])
            mask[x][y] = np.random.random()
    if sigma is not None:
        mask = gaussian(mask, sigma=sigma)
    data += mask * power
    return data