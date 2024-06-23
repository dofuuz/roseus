# Roseus colormap family
# https://github.com/dofuuz/roseus
# matplotlib interface
"""
matplotlib module of Roseus colormaps.

Import roseus.mpl to use with matplotlib. The colormaps will be registered to matplotlib with 'rs.' prefix.

Examples
--------
import matplotlib.pyplot as plt
import roseus.mpl as rs

plt.imshow(x, cmap=rs.arcus)
# or
plt.imshow(x, cmap='rs.arcus')
"""

import os.path as osp

import matplotlib as mpl
import numpy as np
from matplotlib.colors import Colormap, ListedColormap

from .cmap import cmap_names


def register_colormap(name: str, rgb_data) -> tuple[Colormap, Colormap]:
    cmap = ListedColormap(rgb_data, name=f'rs.{name}')
    cmap_r = cmap.reversed()

    mpl.colormaps.register(cmap)
    mpl.colormaps.register(cmap_r)

    return cmap, cmap_r


for name in cmap_names:
    npy_path = osp.join(osp.dirname(__file__), 'cmap', f'{name}.npy')
    rgb_data = np.load(npy_path)
    cmap, cmap_r = register_colormap(name, rgb_data)

    globals()[name] = cmap
    globals()[f'{name}_r'] = cmap_r


__all__ = tuple(cmap_names) + tuple(f'{name}_r' for name in cmap_names)
