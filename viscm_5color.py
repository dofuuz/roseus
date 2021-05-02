# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:16:14 2021

@author: dof
"""

import numpy as np
from matplotlib.colors import LinearSegmentedColormap


cm_name = 'Audicity Light'
cm_data = np.asarray([
    (192/255, 192/255, 192/255),
    (76/255, 153/255, 255/255),
    (229/255, 25/255, 229/255),
    (255/255, 0/255, 0/255),
    (255/255,  255/255, 255/255),
])

# cm_name = 'Magma(5 color)'
# cm_data = np.asarray([
#     (8/255, 0/255, 8/255),
#     (80/255, 0/255, 128/255),
#     (208/255, 32/255, 80/255),
#     (255/255, 160/255, 0/255),
#     (255/255,  255/255, 248/255),
# ])

# cm_name = 'Audacity proposal-alt'
# cm_data = np.asarray([
#     (8/255, 0/255, 8/255),
#     (64/255, 0/255, 144/255),
#     (192/255, 16/255, 176/255),
#     (255/255, 144/255, 32/255),
#     (255/255, 255/255, 248/255),
# ])

# cm_name = 'Audacity proposal(5 color)'
# cm_data = np.asarray([
#     (0/255, 0/255, 8/255),
#     (0/255, 48/255, 144/255),
#     (192/255, 16/255, 176/255),
#     (255/255, 144/255, 32/255),
#     (255/255,  255/255, 248/255),
# ])


test_cm = LinearSegmentedColormap.from_list(cm_name, cm_data)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        from viscm import viscm
        viscm(test_cm)
    except ImportError:
        print("viscm not found, falling back on simple display")
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',
                    cmap=test_cm)
    
    fix, ax = plt.subplots()
    plt.plot(cm_data[:,0], 'r')
    plt.plot(cm_data[:,1], 'g')
    plt.plot(cm_data[:,2], 'b')
    plt.plot(np.mean(cm_data, axis=1))
    ax.set_xticks(np.linspace(0, len(cm_data), len(cm_data), endpoint=False))
    
    ax.grid(which='both')
    plt.show()
