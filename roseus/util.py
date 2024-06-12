from importlib import import_module

from matplotlib.colors import ListedColormap

from .generator import gen_colormap, plot_rgb
from .viscm_cam16ucs import viscm


def plot_measures(name: str):
    mod = import_module(f'roseus.cmap.{name}')
    cm_data, _ = gen_colormap(*mod.gen_props, plots='verbose')

    test_cm = ListedColormap(cm_data, name=f'rs.{name}')

    viscm(test_cm)

    plot_rgb(cm_data)
