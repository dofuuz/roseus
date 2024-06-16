# Roseus colormap family
# https://github.com/dofuuz/roseus
# matplotlib interface

from importlib import import_module

import matplotlib as mpl
from matplotlib.colors import Colormap, ListedColormap

from .cmap import cmap_names


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


__all__ = tuple(cmap_names) + tuple(f'{name}_r' for name in cmap_names)
