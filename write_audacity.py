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

from roseus import gen_colormap


J_RES = 256


def cam16_to_srgb(jab):
    xyz = colour.CAM16UCS_to_XYZ(jab)
    rgb = colour.XYZ_to_sRGB(xyz)
    return rgb


def srgb_to_cam16(rgb):
    xyz = colour.sRGB_to_XYZ(rgb)
    jab = colour.XYZ_to_CAM16UCS(xyz)
    return jab


cm_data, _ = gen_colormap()

# Generate uint8 format colormaps
cm_data_u8 = (cm_data*255 + 0.5).astype('uint8')

cm_selected = cm_data*0.8 + 0.3
cm_selected_u8 = (np.clip(cm_selected, 0, 1)*255 + 0.5).astype('uint8')

cm_jpapbp = srgb_to_cam16(cm_data)
cm_data_JCh = colour.models.Jab_to_JCh(cm_jpapbp)
cm_data_JCh[..., 0] += 20   # Boost lightness
cm_data_JCh[..., 1] += 5   # Boost chroma
cm_data_JCh[..., 2] += 90   # Change hue
cm_data_jab = colour.models.JCh_to_Jab(cm_data_JCh)
cm_sel_freq = cam16_to_srgb(cm_data_jab)
cm_sel_freq_u8 = (np.clip(cm_sel_freq, 0, 1)*255 + 0.5).astype('uint8')


HEAD = '''/**********************************************************************

  Audacity: A Digital Audio Editor

  @file AColorResources.h
  @brief RGB data of 'Color (New)' spectrogram color scheme

  Roseus colormap from
  https://github.com/dofuuz/audacity-colormap

**********************************************************************/


'''


# Save colormaps to C format
with open('generated/AColorResources.h', 'wt') as ofile:
    ofile.write(HEAD)

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
