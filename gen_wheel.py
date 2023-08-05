# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 11:54:56 2021

@author: dof
"""

import math

import colour
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.colors import ListedColormap
from scipy import ndimage
from scipy.signal import savgol_filter


'''
J = lightness
C = chroma
h = hue
'''

# Resolution of colorspace
J_RES = 256
C_RES = 256

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

NAME = 'AudaSpec+'
ANGLE = np.pi * 2 * 0.875
OFFSET = np.pi * 2 * 0.5
CCW = False
SMOOTH = 1/3

DESATURATE = 0.9


def cam16_to_srgb(jab):
    xyz = colour.CAM16UCS_to_XYZ(jab)
    rgb = colour.XYZ_to_sRGB(xyz)
    return rgb


def srgb_to_cam16(rgb):
    xyz = colour.sRGB_to_XYZ(rgb)
    jab = colour.XYZ_to_CAM16UCS(xyz)
    return jab


# Generate CAM02-UCS(Jp, ap, bp) colorspace
j_space = np.linspace(0.1, 99, J_RES)
c_space = np.linspace(0, 50, C_RES)

if CCW:
    h_ = np.linspace(ANGLE+OFFSET, OFFSET, J_RES)
else:
    h_ = np.linspace(OFFSET, ANGLE+OFFSET, J_RES)
h_ = np.degrees(h_)

jch = np.zeros([C_RES, J_RES, 3])
jch[..., 0] = j_space
jch[..., 1] = np.expand_dims(c_space, 1)
jch[..., 2] = h_
jpapbp = colour.models.JCh_to_Jab(jch)

# Convert to sRGB
rgb = cam16_to_srgb(jpapbp)


# Get chroma limit of sRGB
c_limit = np.zeros_like(j_space)
for jdx in range(J_RES):
    max_cdx = 0
    for cdx in range(1, C_RES):
        if np.any(rgb[cdx, jdx] <= 0) or np.any(1 < rgb[cdx, jdx]):
            max_cdx = cdx - 1
            break
        
    c_limit[jdx] = max_cdx


# Smooth chroma limit contour
c_smoothed = np.concatenate([-c_limit[::-1][:-1], c_limit, -c_limit[::-1][1:]])

c_smoothed = savgol_filter(c_smoothed, math.ceil(J_RES*SMOOTH*1.5/2)*2 - 1, 3)
c_smoothed = ndimage.uniform_filter1d(c_smoothed, int(J_RES*SMOOTH*1.5/2)) * DESATURATE

c_smoothed = c_smoothed[J_RES:2*J_RES]

c_selected = c_smoothed.clip(min=0).astype(int)


# Generate and plot gaumt
gamut_image = np.copy(rgb)
gamut_image[gamut_image<=0] = 1
gamut_image[1<gamut_image] = 0

# Mark smoothed contour on image
for jdx, max_c in enumerate(c_selected):
    if 0 == jdx % 2:
        gamut_image[max_c, jdx] = 1
    else:
        gamut_image[max_c, jdx] = 0

plt.figure(figsize=[5, 5])
plt.imshow(gamut_image)


# Get colors on contour
chroma = c_smoothed * 50 / C_RES
cm_data_JCh = np.stack([j_space, chroma, h_], axis=-1)
cm_jpapbp = colour.models.JCh_to_Jab(cm_data_JCh)

cm_rgb = cam16_to_srgb(cm_jpapbp)
cm_data = np.clip(cm_rgb, 0, 1)


# Display viscm
test_cm = ListedColormap(cm_data, name=NAME)

try:
    from viscm import viscm
    viscm(test_cm)
except ImportError:
    print("viscm not found, falling back on simple display")
    plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=test_cm)


# Plot RGB value graph
cm255 = np.asarray(cm_data) * 255
seg_simple = 8

fix, ax = plt.subplots()
plt.plot(cm255[:,0], 'r')
plt.plot(cm255[:,1], 'g')
plt.plot(cm255[:,2], 'b')
plt.plot(np.mean(cm255, axis=1))

ax.set_xticks(np.linspace(0, J_RES, seg_simple+1, endpoint=True))
ax.set_yticks(np.arange(0, 257, 16))

ax.grid(which='both')
plt.show()


# Generate uint8 format colormaps
cm_data_u8 = (cm_data*255 + 0.5).astype('uint8')

cm_selected = cm_rgb*0.8 + 0.3
cm_selected_u8 = (np.clip(cm_selected, 0, 1)*255 + 0.5).astype('uint8')

cm_data_JCh[..., 0] += 20   # Boost lightness
cm_data_JCh[..., 1] += 5   # Boost chroma
cm_data_JCh[..., 2] += 90   # Change hue
cm_data_jab = colour.models.JCh_to_Jab(cm_data_JCh)
cm_sel_freq = cam16_to_srgb(cm_data_jab)
cm_sel_freq_u8 = (np.clip(cm_sel_freq, 0, 1)*255 + 0.5).astype('uint8')

# Save colormaps to C format
with open('AColorResources.h', 'wt') as ofile:
    ofile.write('const unsigned char specColormap[%d][3] = {\n' % J_RES)
    for r, g, b in cm_data_u8:
        ofile.write('   {%3d, %3d, %3d},\n' % (r, g, b))
    ofile.write('};\n\n')

    ofile.write('const unsigned char selColormap[%d][3] = {\n' % J_RES)
    for r, g, b in cm_selected_u8:
        ofile.write('   {%3d, %3d, %3d},\n' % (r, g, b))
    ofile.write('};\n\n')
    
    ofile.write('const unsigned char freqSelColormap[%d][3] = {\n' % J_RES)
    for r, g, b in cm_sel_freq_u8:
        ofile.write('   {%3d, %3d, %3d},\n' % (r, g, b))
    ofile.write('};\n\n')
