# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:18:16 2023

@author: dof
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from roseus.generator import gen_colormap
# from gen_old import cm_data as audaspec_data


CMAP_SETTINGS = [
    ([[-185, 170], 'cos', (2, 99)], 'roseus'),

    # red~magenta
    ([[75, -105], 'sin', (1, 99)], 'r'),

    # blue
    ([[10, -170], 'sin', (2, 99)], 'b'),

    # red blue
    ([[95, -225], 'sin', (2, 99)], 'cyanus'),

    # brown, purble, blue, light green, light yellow
    ([[130, -320], 'sin', (2, 98.5)], 'rbg'),

    # rainbow
    ([[190, -495], 'sin', (2, 99)], 'arcus'),

    # green yellow
    ([[210, 30], 'sin', (2, 98.5)], 'gr'),

    # green
    ([[70, 250], 'sin', (2, 99)], 'rg'),

    # blue, pink
    ([[-125, 45], 'sin', (2, 98.5)], 'lavendula'),
]

if __name__ == '__main__':
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    cmap_list = []
    for (h, C, L), cm_name in CMAP_SETTINGS:
        cm_data, _ = gen_colormap(h, C, L)
        cm = mpl.colors.ListedColormap(cm_data, name=cm_name)
        cmap_list.append(cm)

    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22  # + 0.2
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.3, right=0.99)
    axs[0].set_title('Roseus colormap family', fontsize=14)

    for ax, cmap in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    plt.show()
