# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:15:42 2023

@author: kt
"""

import colour
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap


RES = 100000
POINTS = 256


def gen_colormap(hue_range=(-110, 115)):
    J_MIN = 3
    J_MAX = 98

    rx = np.linspace(0, 1, RES)

    # Smooth square wave https://dsp.stackexchange.com/a/56529
    # delta = 1
    # r = 1 / np.arctan(1/delta) * np.arctan(np.sin(np.pi * rx) / delta)

    # Sine
    # r = np.sin(np.pi * rx)

    # Half circle
    r = np.sqrt(1 - (1 - 2*rx) * (1 - 2*rx))

    # plt.plot(r)

    # blue to yellow -77 ~ 111
    # AudaSpec1 = -180 ~ 135
    h = np.linspace(hue_range[0], hue_range[1], RES)
    h_rad = np.radians(h)

    a = r * np.cos(h_rad)
    b = r * np.sin(h_rad)

    plt.figure()
    plt.plot(a, b)
    plt.axis('equal')

    a_diff = np.diff(a)
    b_diff = np.diff(b)

    len_ab = np.hypot(a_diff, b_diff)
    cumsum_len = np.cumsum(len_ab)
    sum_len = cumsum_len[-1]

    last = 0
    cdx = 0  # index of coordinate
    idx_sel = []
    for idx in range(len(cumsum_len)):
        length = sum_len * cdx / POINTS
        if last <= length < cumsum_len[idx]:
            if length - last < cumsum_len[idx] - length:
                idx_sel.append(idx)
            else:
                idx_sel.append(idx+1)

            cdx += 1

        if POINTS <= cdx:
            break

    j = np.linspace(J_MIN, J_MAX, len(idx_sel))

    for c_mul in np.arange(40, 20, -0.1):
        c_ = r[idx_sel] * c_mul
        h_ = h[idx_sel]
        jch = np.stack([j, c_, h_], axis=-1)

        jab = colour.models.JCh_to_Jab(jch)
        # xyz = colour.CAM02UCS_to_XYZ(jab)
        xyz = colour.CAM16UCS_to_XYZ(jab)
        color_rgb = colour.XYZ_to_sRGB(xyz)

        if 0 <= np.min(color_rgb) and np.max(color_rgb) <= 1:
            break

    len_arc = sum_len * c_mul * (J_MAX - J_MIN)
    print(len_arc)

    # plt.figure()
    # plt.plot(c_)
    # plt.plot(h_)

    return color_rgb, len_arc


if __name__ == "__main__":
    color_rgb, _ = gen_colormap()
    cm_data = np.clip(color_rgb, 0, 1)

    test_cm = ListedColormap(cm_data, name='AudaSpec2')
    try:
        from viscm import viscm
        viscm(test_cm)
    except ImportError:
        print("viscm not found, falling back on simple display")
        plt.figure()
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=test_cm)

    rgbs = (color_rgb*255).round().clip(0, 255).astype('uint8')
