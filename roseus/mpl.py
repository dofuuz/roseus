# Roseus colormap family
# https://github.com/dofuuz/roseus

from importlib import import_module

import matplotlib as mpl
from matplotlib.colors import Colormap, ListedColormap


cmap_names = [
    'roseus',
    'r',
    'b',
    'cyanus',
    'rbg',
    'arcus',
    'gr',
    'rg',
    'lavendula',
]


def register_colormap(name: str, rgb_data) -> tuple[Colormap, Colormap]:
    cmap = ListedColormap(rgb_data, name=f'rs.{name}')
    cmap_r = cmap.reversed()

    mpl.colormaps.register(cmap)
    mpl.colormaps.register(cmap_r)

    return cmap, cmap_r


for name in cmap_names:
    mod = import_module(f'roseus.cmap.{name}')
    cmap, cmap_r = register_colormap(name, mod.rgb_data)

    globals()[name] = cmap
    globals()[f'{name}_r'] = cmap_r
