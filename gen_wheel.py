# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 11:54:56 2021

@author: dof
"""


import colorspacious
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.colors import ListedColormap
from scipy.ndimage import filters


'''
J = lightness
C = chroma
h = hue
'''

# Resolution of colorspace
J_RES = 512
C_RES = 512

# NAME = 'So normal'
# ANGLE = np.pi * 2 * 0.7
# OFFSET = np.pi * 2 * 0.64
# CCW = False
# SMOOTH = 1/3

# NAME = 'Wow unique'
# ANGLE = np.pi * 2 * 1.0
# OFFSET = np.pi * 2 * 0.275
# CCW = True
# SMOOTH = 1/2

# NAME = 'Viridis-like (red bg)'
# ANGLE = np.pi * 2 * 1.0
# OFFSET = np.pi * 2 * 0.1
# CCW = True
# SMOOTH = 1/4

# NAME = 'Viridis-like (purple bg)'
# ANGLE = np.pi * 2 * 0.9
# OFFSET = np.pi * 2 * 0.1
# CCW = True
# SMOOTH = 1/5

NAME = 'Audacity proposal'
ANGLE = np.pi * 2 * 0.85
OFFSET = np.pi * 2 * 0.5
CCW = False
SMOOTH = 1/4


j_space = np.linspace(1, 101, J_RES)
c_space = np.linspace(0, 50, C_RES)

if CCW:
    h_ = np.linspace(ANGLE+OFFSET, OFFSET, J_RES)
else:
    h_ = np.linspace(OFFSET, ANGLE+OFFSET, J_RES)

jpapbp = np.zeros([C_RES, J_RES, 3])
for jdx, jp in enumerate(j_space):
    for cdx, chroma in enumerate(c_space):
        ap = np.cos(h_[jdx]) * chroma
        bp = np.sin(h_[jdx]) * chroma
        jpapbp[cdx, jdx] = (jp, ap, bp)

rgb = colorspacious.cspace_convert(jpapbp, "CAM02-UCS", "sRGB255")

c_limit = np.zeros_like(j_space)
for jdx in range(J_RES):
    max_cdx = 0
    for cdx in range(C_RES):
        if np.any(rgb[cdx, jdx] < 0) or np.any(255 < rgb[cdx, jdx]):
            max_cdx = cdx - 1
            break
        
    c_limit[jdx] = max_cdx

c_smoothed = filters.uniform_filter1d(c_limit, int(J_RES*SMOOTH), mode='constant', cval=-(C_RES*SMOOTH))
# c_limit = np.min(np.vstack((c_limit, c_smoothed)), axis=0)
c_selected = c_smoothed.clip(min=0).astype(int)

gamut_image = np.asarray(rgb, dtype=int)
gamut_image[gamut_image<0] = 255
gamut_image[255<gamut_image] = 0


cm_data = []
for jdx, max_c in enumerate(c_selected):
    cm_data.append(rgb[max_c, jdx]/255)
    gamut_image[max_c, jdx] = 128
cm_data = np.clip(cm_data, 0, 1)

plt.imshow(gamut_image)


test_cm = ListedColormap(cm_data, name=NAME)

try:
    from viscm import viscm
    viscm(test_cm)
except ImportError:
    print("viscm not found, falling back on simple display")
    plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=test_cm)

cm255 = np.asarray(cm_data) * 255
seg_simple = 5

plt.figure()
fix, ax = plt.subplots()
plt.plot(cm255[:,0], 'r')
plt.plot(cm255[:,1], 'g')
plt.plot(cm255[:,2], 'b')
plt.plot(np.mean(cm255, axis=1))
# plt.plot(np.arange(0, 257, 256/seg_simple), np.asarray(cm_simplified)*256)
# plt.plot(np.arange(0, 257, 256/seg_simple), np.mean(np.asarray(cm_simplified)*256, axis=1))
ax.set_xticks(np.linspace(0, 512, seg_simple, endpoint=False))
ax.set_yticks(np.arange(0, 257, 16))

ax.grid(which='both')
plt.show()

cm_data_u8 = (cm_data*255).astype('uint8')
with open('AColorResources.h', 'wt') as output_file:
    print('const unsigned char spectroGradient[512][3] = {', file=output_file)
    for r, g, b in cm_data_u8:
        print('   {%3d, %3d, %3d},' % (r, g, b), file=output_file)
    print('};', file=output_file)
