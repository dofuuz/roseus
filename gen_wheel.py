# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 08:57:50 2021

@author: dof
"""

from colorspacious import cspace_converter, cspace_convert, CIECAM02Space
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

h_len = len(np.arange(0, 100.1, 1))
C_h_ = np.mgrid[0:100.1:1, 0:400.1:1].reshape(2, h_len, -1).T
J_ = np.ones(C_h_.shape[:-1]) * 50
J_ = np.expand_dims(J_, 2)

J_C_h = np.concatenate([J_, C_h_], axis=2)

rgb = cspace_convert(J_C_h, "JCh", "sRGB1")
rgb[rgb<0] = 1
rgb[1<rgb] = 0

# plt.imshow(rgb)

offset = 150
J_ = np.linspace(0, 100, 256)
h_ = np.linspace(0+offset, 360+offset, 256)

JCh = np.zeros((100, 256, 3))
for idx in range(0, 256):
    for cdx in range(0, 100):
        JCh[cdx, idx] = (J_[idx], cdx, h_[idx])

rgb2 = cspace_convert(JCh, "JCh", "sRGB255")

c_limit = np.zeros_like(J_, dtype=int)
for idx in range(len(J_)):
    max_c = 99
    for cdx in range(100):
        if np.any(rgb2[cdx, idx] < 0) or np.any(255 < rgb2[cdx, idx]):
            max_c = cdx - 1
            break
        
    c_limit[idx] = max(0, max_c)

c_limit_smoothed = scipy.ndimage.filters.uniform_filter1d(c_limit, 40, mode='constant')
c_limit = np.min(np.vstack((c_limit, c_limit_smoothed)), axis=0)

rgb2_ = np.asarray(rgb2, dtype=int)
rgb2_[rgb2_<0] = 255
rgb2_[255<rgb2_] = 0

cm_data = []
for idx, max_c in enumerate(c_limit):
    cm_data.append(rgb2[max_c, idx]/255)
    rgb2_[max_c, idx] = 128
cm_data = np.clip(cm_data, 0, 1)

plt.imshow(rgb2_)



from matplotlib.colors import ListedColormap, LinearSegmentedColormap
test_cm = ListedColormap(cm_data, name="vividis")

import matplotlib.pyplot as plt
import numpy as np

try:
    from viscm import viscm
    viscm(test_cm)
except ImportError:
    print("viscm not found, falling back on simple display")
    plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',
                cmap=test_cm)
plt.show()

plt.figure()
fix, ax = plt.subplots()
plt.plot(np.asarray(cm_data)*256)
plt.plot(np.mean(np.asarray(cm_data)*256, axis=1))
# plt.plot(np.arange(0, 257, 256/seg_simple), np.asarray(cm_simplified)*256)
# plt.plot(np.arange(0, 257, 256/seg_simple), np.mean(np.asarray(cm_simplified)*256, axis=1))
# ax.set_xticks(np.arange(0, 256, 256/seg_simple))
ax.set_yticks(np.arange(0, 256, 16))

ax.grid(which='both')
plt.show()
