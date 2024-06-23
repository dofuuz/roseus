# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:00:46 2023

@author: dof
"""

import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import maximum_filter

import roseus.mpl as rs
from roseus.generator import gen_colormap


def batch_colormap(tasks):
    results = []
    for task in tasks:
        _, score = gen_colormap(task, chroma_shape='sin', lightness_range=(2, 98))
        results.append(score)
    return results


if __name__ == '__main__':
    mp.freeze_support()

    # sr = (-180, 180)
    # rr = (60, 600)
    sr = (0, 360)
    rr = (-600, -60)

    start_space = np.arange(sr[0], sr[1], 5)
    # start_space = np.arange(-180, -90, 2)
    range_space = np.arange(rr[0], rr[1], 10)
    # range_space = np.arange(210, 300, 5)
    
    task_list = []
    for sdx, s in enumerate(start_space):
        l = []
        for rdx, r in enumerate(range_space):
            l.append([s, s+r])
        task_list.append(l)
    
    with mp.Pool(processes=8) as p:
        results = p.map(batch_colormap, task_list)
    
    arc_scores = np.asarray(results, dtype=np.float32)

    plt.imshow(arc_scores.T, extent=(sr[0], sr[1], rr[1], rr[0]), interpolation='none', cmap=rs.roseus)

    max_index = np.unravel_index(arc_scores.argmax(), arc_scores.shape)
    print(max_index)

    s = start_space[max_index[0]]
    r = range_space[max_index[1]]
    
    print([s, s+r])
    print(arc_scores.max())

    # find local maxima
    mx = maximum_filter(arc_scores, size=5, mode='wrap')
    local_maxima = np.where(mx == arc_scores, arc_scores, 0)

    for sdx, rs in enumerate(local_maxima):
        for rdx, maxima in enumerate(rs):
            if maxima:
                s = start_space[sdx]
                r = range_space[rdx]
                
                print(f'{[s, s+r]}: {maxima}')


## score = arc_len
# Smooth square wave(delta=1)
# [-132, 138]: 14460.9091763
# [-180, 290]: 14997.7752763
# [ 90, -220]: 13885.7844931
# [130, -340]: 14455.6870133

# sin
# -140, 150: 14422.0391652
# [-142, 153]: 14470.7520561
#  170, 630: 14641.5163216
# 140, -330: 14450.0564754
# 100, -230: 14105.945636

# circle
# [-150, 320]: 15800.0729142
# [-110, 115]: 14254.3959554
# [80, -390]: 14834.1295919
# [80, -280]: 14073.892873


## score = arc_len * c_mul
# circle
# [50, -70]: 408559.46875 red
# [60, -190]: 444375.125 brown, purple, cyan, light green
# [80, -270]: 362282.96875 brown, purble, blue, light green, light yellow
# [100, -410]: 341647.0
# [110, -490]: 350433.625
# [170, 90]: 206177.3125
# [190, 20]: 196225.375
# [195, -5]: 198383.8125
# [215, -155]: 229608.78125

# [-155, 375]: 369652.75
# [-150, 330]: 365042.96875
# [-145, 285]: 366187.625
# [-110, 110]: 512811.90625 blue, magenta, orange, yellow
# [-100, 20]: 432491.375 blue, pink
# [55, 385]: 212308.265625
# [75, 285]: 194046.671875
# [115, 175]: 204104.5

# square (delta=0.2)
# [45, -65]: 395497.84375 red
# [55, -175]: 428418.3125 red blue
# [60, -190]: 407844.90625
# [70, -250]: 364064.34375
# [75, -295]: 354519.4375 brown, purple, blue, light green, light yellow
# [90, -450]: 355342.1875 rainbow
# [165, 85]: 195226.9375
# [180, 10]: 195549.828125
# [190, -70]: 205483.78125

# [-140, 360]: 376395.25
# [-135, 305]: 373645.25
# [-130, 260]: 372501.8125
# [-125, 215]: 378041.90625
# [-95, 5]: 426754.28125 blue, pink
# [-95, 95]: 480429.6875 blue, magenta, orange, yellow
# [85, 335]: 192416.578125
# [90, 300]: 188870.765625
# [95, 265]: 185565.96875
# [100, 240]: 185357.625
# [120, 180]: 192212.265625

# sin
# [75, -105]: 426427.21875 red~magenta
# [100, -230]: 465496.21875 red, blue
# [175, -425]: 366657.25  brown, purble, blue, light green, light yellow
# [215, 15]: 202833.59375
# [305, -295]: 285954.3125

# [-140, 150]: 535061.5625 blue, magenta, orange, yellow
# [-125, 45]: 443523.875 blue pink
# [40, 300]: 204412.046875
# [50, 280]: 202630.34375
# [60, 260]: 201245.859375
# [75, 235]: 200493.0625
# [90, 210]: 206164.40625
# [145, 705]: 379349.03125
# [155, 675]: 380382.5625
