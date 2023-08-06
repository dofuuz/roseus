# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:15:42 2023

@author: kt
"""

import colour
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap


RES = 2 ** 20
POINTS = 256


def gen_colormap(hue_range=(-110, 115), chroma_shape='circle', lightness_range=(3, 97), plots=False):
    rx = np.linspace(0, 1, RES)

    if chroma_shape == 'square':
        # https://dsp.stackexchange.com/a/56529
        delta = 0.2
        c = 1 / np.arctan(1/delta) * np.arctan(np.sin(np.pi * rx) / delta)

    elif chroma_shape == 'sin':
        c = np.sin(np.pi * rx)

    elif chroma_shape == 'circle':
        c = np.sqrt(1 - (1 - 2*rx) * (1 - 2*rx))

    # if plots:
    #     plt.plot(c)

    h = np.linspace(hue_range[0], hue_range[1], RES)
    h_rad = np.radians(h)

    # get ab arc
    a = c * np.cos(h_rad)
    b = c * np.sin(h_rad)

    # if plots:
    #     plt.figure()
    #     plt.plot(a, b)
    #     plt.axis('equal')

    # differentiate ab arc
    diff_ab = np.hypot(np.diff(a), np.diff(b))
    cumsum_ab = np.cumsum(diff_ab)
    sum_len = cumsum_ab[-1]

    last_cumsum = 0
    idx_sel = []
    idx = 0
    for cdx in range(POINTS):
        length = sum_len * cdx / POINTS
        while True:
            cumsum = cumsum_ab[idx]
            if last_cumsum <= length < cumsum:
                break
            idx += 1

        if length - last_cumsum < cumsum - length:
            idx_sel.append(idx)
        else:
            idx_sel.append(idx+1)

    j = np.linspace(lightness_range[0], lightness_range[1], POINTS)

    for c_mul in np.arange(45, 0, -0.1):
        if c_mul < 20:
            return None, sum_len * c_mul * (lightness_range[1] - lightness_range[0])
        c_ = c[idx_sel] * c_mul
        h_ = h[idx_sel]
        jch = np.stack([j, c_, h_], axis=-1)

        jab = colour.models.JCh_to_Jab(jch)
        # xyz = colour.CAM02UCS_to_XYZ(jab)
        xyz = colour.CAM16UCS_to_XYZ(jab)
        color_rgb = colour.XYZ_to_sRGB(xyz)

        if 0 <= np.min(color_rgb) and np.max(color_rgb) <= 1:
            break

    arc_len = sum_len * c_mul * (lightness_range[1] - lightness_range[0])

    if plots:
        print(c_mul)
        print(arc_len)
    
        # plt.figure()
        # plt.plot(c_)
        # plt.plot(h_)

    return color_rgb, arc_len * c_mul


if __name__ == "__main__":
    # hue range
    # blue to yellow -77, 111
    # AudaSpec1 = -180, 135

    # red~magenta
    # color_rgb, _ = gen_colormap(hue_range=(50,  -70), chroma_shape='circle', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[45, -65], chroma_shape='square', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[75, -105], chroma_shape='sin', plots=True)

    # red blue
    # color_rgb, _ = gen_colormap(hue_range=[55, -175], chroma_shape='square', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[100, -230], chroma_shape='sin', plots=True)

    # brown, purple, cyan, light green
    # color_rgb, _ = gen_colormap(hue_range=(100, -230), chroma_shape='sin', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=(60, -190), chroma_shape='circle', plots=True)

    # brown, purble, blue, light green, light yellow
    # color_rgb, _ = gen_colormap(hue_range=(80, -270), chroma_shape='circle', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=(75, -295), chroma_shape='square', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[175, -425], chroma_shape='sin', plots=True)

    # rainbow
    # color_rgb, _ = gen_colormap(hue_range=(90, -450), chroma_shape='square', plots=True)

    # blue, pink
    # color_rgb, _ = gen_colormap(hue_range=(-100, 20), chroma_shape='circle', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[-95, 5], chroma_shape='square', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[-125, 45], chroma_shape='sin', plots=True)

    # blue, magenta, orange, yellow
    # color_rgb, _ = gen_colormap(hue_range=(-110, 110), lightness_range=(3, 98), chroma_shape='circle', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[-95, 95], lightness_range=(3, 98), chroma_shape='square', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[-140, 150], lightness_range=(3, 98), chroma_shape='sin', plots=True)

    # color_rgb, _ = gen_colormap(hue_range=(-115, 100), lightness_range=(3, 98), chroma_shape='circle', plots=True)
    # color_rgb, _ = gen_colormap(hue_range=[-100, 85], lightness_range=(3, 98), chroma_shape='square', plots=True)
    color_rgb, _ = gen_colormap(hue_range=[-150, 135], lightness_range=(3, 98), chroma_shape='sin', plots=True)


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

    seg_simple = 8

    fix, ax = plt.subplots()
    plt.plot(rgbs[:,0], 'r')
    plt.plot(rgbs[:,1], 'g')
    plt.plot(rgbs[:,2], 'b')
    plt.plot(np.mean(rgbs, axis=1))

    ax.set_xticks(np.linspace(0, len(cm_data), seg_simple+1, endpoint=True))
    ax.set_yticks(np.arange(0, 257, 16))

    ax.grid(which='both')
    plt.show()
