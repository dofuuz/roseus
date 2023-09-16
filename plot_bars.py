# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:18:16 2023

@author: dof
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from roseus import gen_colormap
from gen_old import cm_data as audaspec_data


CMAP_SETTINGS = [
    # red~magenta
    [[50, -70], 'circle', (3, 97)],
    [[45, -65], 'square', (3, 97)],
    [[75, -105], 'sin', (3, 97)],

    # red blue
    [[55, -175], 'square', (3, 97)],
    [[100, -230], 'sin', (3, 97)],

    # brown, purple, cyan, light green
    [[100, -230], 'sin', (3, 97)],
    [[60, -190], 'circle', (3, 97)],

    # brown, purble, blue, light green, light yellow
    [[80, -270], 'circle', (3, 97)],
    [[75, -295], 'square', (3, 97)],
    [[175, -425], 'sin', (3, 97)],

    # rainbow
    [[90, -450], 'square', (3, 99)],

    # blue, pink
    [[-100, 20], 'circle', (3, 97)],
    [[-95, 5], 'square', (3, 97)],
    [[-125, 45], 'sin', (3, 97)],

    # blue, magenta, orange, yellow
    [[-180, 135], 'cos', (2, 98)],
    [[-109, 115], 'circle', (2, 98)],  # optimal
    [[-114, 108], 'circle', (2, 98)],
    [[-95, 95], 'square', (3, 98)],
    [[-105, 95], 'square', (2, 98.5)],
    [[-139, 138], 'sin', (2, 99)],  # optimal
    [[-144, 138], 'sin', (2, 99)],
    [[-150, 135], 'sin', (5, 99)],
    [[-185, 189], 'cos', (2, 99)],  # optimal

    [[-115, 100], 'circle', (3, 98)],
    [[-100, 85], 'square', (1, 97)],
    [[-150, 135], 'sin', (3, 99)],
]


gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

cmap_list = []
for h, C, L in CMAP_SETTINGS:
    cm_data, _ = gen_colormap(h, C, L)
    cm = mpl.colors.ListedColormap(cm_data, name=f'{L} {C} {h}')
    cmap_list.append(cm)

cmap_list.append(mpl.colors.ListedColormap(audaspec_data, name='v0.1'))
cmap_list.append(mpl.colors.ListedColormap(gen_colormap()[0], name='Roseus'))

# Create figure and adjust figure height to number of colormaps
nrows = len(cmap_list)
figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22  # + 0.2
fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                    left=0.3, right=0.99)
axs[0].set_title('Findings and candiates', fontsize=14)

for ax, cmap in zip(axs, cmap_list):
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
            transform=ax.transAxes)

# Turn off *all* ticks & spines, not just the ones with colormaps.
for ax in axs:
    ax.set_axis_off()

plt.show()
