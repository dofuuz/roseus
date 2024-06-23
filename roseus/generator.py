# -*- coding: utf-8 -*-
"""
Roseus colormap generator
https://github.com/dofuuz/roseus

Roseus: Perceptually uniform colormaps with full range of lightness
"""

import bisect

import colour
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap


RES = 2 ** 20
POINTS = 256


def gen_colormap(hue_range=(-185, 170), chroma_shape='cos', lightness_range=(2, 99), plots=False):
    """ Generate a perceptually uniform colormap has symmetric and smooth chroma, hue transition.

    Parameters
    ----------
    hue_range : tuple
        Hue range in degrees.
    chroma_shape :
        Shape of chroma transition.
        One of 'sin', 'circle', 'cos'.
    lightness_range : tuple
        Lightness range
    plots :
        Set `True` to print details.
        Set 'verbose' to print additional measures.

    Returns
    -------
        Tuple of (color_rgb, score).
        `color_rgb` is RGB values of the colormap.
        `score` is value represents how much colormap is colorful.
    """
    rx = np.linspace(0, 1, RES)

    if chroma_shape == 'square':
        # https://dsp.stackexchange.com/a/56529
        delta = 0.2
        c = 1 / np.arctan(1/delta) * np.arctan(np.sin(np.pi * rx) / delta)

    elif chroma_shape == 'sin':
        c = np.sin(np.pi * rx)

    elif chroma_shape == 'circle':
        c = np.sqrt(1 - (1 - 2*rx) * (1 - 2*rx))

    elif chroma_shape == 'cos':  # cardioid
        c = (1 - np.cos(2 * np.pi * rx)) / 2

    h = np.linspace(hue_range[0], hue_range[1], RES)
    h_rad = np.radians(h)

    # get ab arc
    a = c * np.cos(h_rad)
    b = c * np.sin(h_rad)

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

    def in_gamut(c_mul):
        c_ = c[idx_sel] * c_mul
        h_ = h[idx_sel]
        jch = np.stack([j, c_, h_], axis=-1)

        jab = colour.models.JCh_to_Jab(jch)
        xyz = colour.CAM16UCS_to_XYZ(jab)
        color_rgb = colour.XYZ_to_sRGB(xyz)

        return 0 <= np.min(color_rgb) and np.max(color_rgb) <= 1

    # search c_mul threshold
    c_mul_space = np.arange(45, 20, -0.1)
    cx = bisect.bisect(c_mul_space, False, key=in_gamut)
    if len(c_mul_space) <= cx:
        return None, sum_len * 20 * (lightness_range[1] - lightness_range[0])

    # desaturate into sRGB gamut
    c_mul = c_mul_space[cx]
    c_ = c[idx_sel] * c_mul
    h_ = h[idx_sel]
    jch = np.stack([j, c_, h_], axis=-1)

    jab = colour.models.JCh_to_Jab(jch)
    xyz = colour.CAM16UCS_to_XYZ(jab)
    color_rgb = colour.XYZ_to_sRGB(xyz)

    arc_len = sum_len * c_mul * (lightness_range[1] - lightness_range[0])

    if plots:
        print(f'Max chroma: {c_mul}')
        print(f'Length of variation: {arc_len}')

    if plots == 'verbose':
        plot_jch(j, c_, h_)
        # plot_gamut(jab)

    return color_rgb, arc_len * c_mul


def plot_jch(j, c_, h_):
    """ Plot transition of Lightness, Chroma, Hue """
    plt.figure(figsize=(6.4, 3.6))

    ax = plt.subplot(231)
    ax.plot(j)
    ax.set_title('Lightness')
    ax.get_xaxis().set_visible(False)

    ax = plt.subplot(232)
    ax.plot(c_)
    ax.set_title('Chroma')
    ax.get_xaxis().set_visible(False)

    ax = plt.subplot(233)
    ax.plot(h_)
    ax.set_title('Hue')
    ax.get_xaxis().set_visible(False)

    ax = plt.subplot(234)
    ax.plot(np.diff(j).astype(np.float32))
    ax.set_title('ΔLightness')
    ax.get_xaxis().set_visible(False)

    ax = plt.subplot(235)
    ax.plot(np.diff(c_))
    ax.set_title('ΔChroma')
    ax.get_xaxis().set_visible(False)

    ax = plt.subplot(236)
    ax.plot(np.diff(h_[1:]))
    ax.set_title('ΔHue')
    ax.get_xaxis().set_visible(False)

    plt.show()


def plot_gamut(jab):
    """ Plot sRGB gamut for colormaps. It is broken for most of colormaps for now."""
    j = jab[..., 0]
    a = jab[..., 1]
    b = jab[..., 2]
    lightness_range = (j[0], j[-1])
    h_ = np.degrees(np.arctan2(b, a))

    # CAM16 Jab colorspace
    ac = np.linspace(-45, 45, 1000)
    bc = np.linspace(-35, 35, 1000)
    ac, bc = np.meshgrid(ac, bc)
    phi = np.degrees(np.arctan2(bc, ac))

    jc = np.searchsorted(h_, phi) / POINTS * (lightness_range[1] - lightness_range[0]) + lightness_range[0]

    xyzs = colour.CAM16UCS_to_XYZ(np.stack([jc, ac, bc], axis=-1))
    rgbs = colour.XYZ_to_sRGB(xyzs)

    # get sRGB gamut
    r = rgbs[..., 0]
    g = rgbs[..., 1]
    b = rgbs[..., 2]
    clipped = np.any([r<0, g<0, b<0, 1<r, 1<g, 1<b], axis=0)
    clipped = np.stack([clipped, clipped, clipped], axis=-1)

    rgbs[clipped] = 0.4426

    # plot gamut
    ax = plt.subplot()
    ax.plot(jab[..., 1], jab[..., 2])
    ax.axis('equal')

    ax.imshow(rgbs, extent=[ac.min(), ac.max(), bc.max(), bc.min()])
    ax.invert_yaxis()
    ax.set_title('sRGB color gamut in CAM16-UCS')
    ax.set_xlabel("a' (green → red)")
    ax.set_ylabel("b' (blue → yellow)")
    plt.show()


def plot_rgb(rgb1):
    """ Plot RGB values """
    rgbs = (rgb1*255).round().clip(0, 255).astype('uint8')

    seg_simple = 8

    fix, ax = plt.subplots()
    plt.plot(rgbs[:,0], 'r')
    plt.plot(rgbs[:,1], 'g')
    plt.plot(rgbs[:,2], 'b')
    plt.plot(np.mean(rgbs, axis=1))
    plt.title('R, G, B and mean(RGB)')

    ax.tick_params(labelbottom=False)
    ax.set_xticks(np.linspace(0, len(rgb1), seg_simple+1, endpoint=True))
    ax.set_yticks(np.arange(0, 257, 16))

    ax.grid(which='both')
    plt.show()


if __name__ == "__main__":
    PLOTS = 'verbose'

    plt.rcParams['figure.autolayout'] = True

    # hue range
    # blue to yellow -77, 111
    # AudaSpec1 = -180, 135

    # red~magenta
    # color_rgb, _ = gen_colormap([50, -70], 'circle', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([45, -65], 'square', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([75, -105], 'sin', (1, 99), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([105, -140], 'cos', (1, 98.5), plots=PLOTS)
    # color_rgb, _ = gen_colormap([125, -180], 'cos', (2, 98.5), plots=PLOTS)

    # red blue
    # color_rgb, _ = gen_colormap([55, -175], 'square', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([95, -225], 'sin', (2, 99), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([110, -225], 'sin', (2, 99), plots=PLOTS)
    # color_rgb, _ = gen_colormap([60, -190], 'circle', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([145, -285], 'cos', (1, 98.5), plots=PLOTS)

    # brown, purble, blue, light green, light yellow
    # color_rgb, _ = gen_colormap([80, -270], 'circle', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([75, -295], 'square', (2, 98.5), plots=PLOTS)
    # color_rgb, _ = gen_colormap([130, -320], 'sin', (2, 98.5), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([-180, -730], 'cos', (2, 98.5), plots=PLOTS)
    # color_rgb, _ = gen_colormap([-170, -720], 'cos', (2, 98.5), plots=PLOTS)

    # rainbow
    # color_rgb, _ = gen_colormap([175, -425], 'sin', (2, 98.5), plots=PLOTS)
    # color_rgb, _ = gen_colormap([190, -495], 'sin', (2, 99), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([-70, -945], 'cos', (2, 99), plots=PLOTS)
    # color_rgb, _ = gen_colormap([-45, -945], 'cos', (2, 99), plots=PLOTS)
    # color_rgb, _ = gen_colormap((90, -450), 'square', (3, 99), plots=PLOTS)

    # blue, pink
    # color_rgb, _ = gen_colormap((-100, 20), 'circle', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([-95, 5], 'square', (3, 97), plots=PLOTS)
    # color_rgb, _ = gen_colormap([-125, 45], 'sin', (2, 98.5), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([-155, 75], 'cos', (2, 98.5), plots=PLOTS)

    # blue, magenta, orange, yellow
    # color_rgb, _ = gen_colormap([-139, 138], 'sin', lightness_range=(2, 99), plots=PLOTS)  # optimal
    # color_rgb, _ = gen_colormap([-185, 189], 'cos', lightness_range=(2, 99), plots=PLOTS)  # optimal
    color_rgb, _ = gen_colormap([-185, 170], 'cos', lightness_range=(2, 99), plots=PLOTS)
    # color_rgb, _ = gen_colormap([-180, 160], 'cos', lightness_range=(2, 99), plots=PLOTS)

    # color_rgb, _ = gen_colormap([10, -170], 'sin', (2, 99), plots=PLOTS)  # v

    # color_rgb, _ = gen_colormap([210, 30], 'sin', (2, 98.5), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([-135, -335], 'cos', (2, 98.5), plots=PLOTS)

    # color_rgb, _ = gen_colormap([-75, 105], 'sin', (2, 98), plots=PLOTS)

    # color_rgb, _ = gen_colormap([70, 250], 'sin', (2, 99), plots=PLOTS)  # v
    # color_rgb, _ = gen_colormap([45, 265], 'cos', (2, 99), plots=PLOTS)

    cm_data = np.clip(color_rgb, 0, 1)

    test_cm = ListedColormap(cm_data, name='Roseus')

    from .viscm_cam16ucs import viscm
    viscm(test_cm)

    plot_rgb(color_rgb)
