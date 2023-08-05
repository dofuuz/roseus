# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:00:46 2023

@author: dof
"""

import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np

from audaspec2 import gen_colormap


def batch_colormap(tasks):
    results = []
    for task in tasks:
        _, score = gen_colormap(task)
        results.append(score)
    return results


if __name__ == '__main__':
    mp.freeze_support()

    # start_space = np.arange(-180, 180, 10)
    start_space = np.arange(-180, -90, 2)
    # range_space = np.arange(-120, -360, -10)
    range_space = np.arange(210, 300, 5)
    
    task_list = []
    for sdx, s in enumerate(start_space):
        l = []
        for rdx, r in enumerate(range_space):
            l.append([s, s+r])
        task_list.append(l)
    
    with mp.Pool() as p:
        results = p.map(batch_colormap, task_list)
    
    arc_scores = np.asarray(results)
    
    plt.imshow(arc_scores.T, extent=[-180, -90, 360, 180], interpolation='none')
    max_index = np.unravel_index(arc_scores.argmax(), arc_scores.shape)
    print(max_index)
    
    s = start_space[max_index[0]]
    r = range_space[max_index[1]]
    
    print([s, s+r])
    print(arc_scores.max())

# Smooth square wave(delta=1)
# [-132, 138]:14460.9091763
# -130, 130: 14260.970709403307
# -180, 290: 14997.7752763
#  90, -220: 13885.7844931
# 130, -340: 14455.6870133

# sin
# -140, 150: 14422.0391652
# [-142, 153]: 14470.7520561
#  170, 630: 14641.5163216
# 140, -330: 14450.0564754
# 100, -230: 14105.945636

# circle
# [-150, 320]: 15800.0729142
# [-110, 115]: 14254.3959554
# [-110, 110]: 14166.0739786
# [80, -390]: 14834.1295919
# [80, -270]: 14041.9748739
