# This file is part of viscm
# https://github.com/matplotlib/viscm

# Copyright (C) 2015 Nathaniel Smith <njs@pobox.com>
# Copyright (C) 2015 Stefan van der Walt <stefanv@berkeley.edu>

# Copyright (c) 2014-2016 the viscm developers
# The MIT License (MIT)

# Modified to use CAM16-UCS instead of CAM02-UCS

import os.path

import colour
import matplotlib
import matplotlib.colors
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import numpy as np
from colorspacious import (
    cspace_convert,
    cspace_converter,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# matplotlib.rcParams['backend'] = "QtAgg"
# Do this first before any other matplotlib imports, to force matplotlib to
# use a Qt backend
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec


GREYSCALE_CONVERSION_SPACE = "JCh"

_sRGB1_to_JCh = cspace_converter("sRGB1", GREYSCALE_CONVERSION_SPACE)
_JCh_to_sRGB1 = cspace_converter(GREYSCALE_CONVERSION_SPACE, "sRGB1")


def to_greyscale(sRGB1):
    JCh = _sRGB1_to_JCh(sRGB1)
    JCh[..., 1] = 0
    return np.clip(_JCh_to_sRGB1(JCh), 0, 1)


_deuter50_space = {"name": "sRGB1+CVD", "cvd_type": "deuteranomaly", "severity": 50}
_deuter50_to_sRGB1 = cspace_converter(_deuter50_space, "sRGB1")
_deuter100_space = {"name": "sRGB1+CVD", "cvd_type": "deuteranomaly", "severity": 100}
_deuter100_to_sRGB1 = cspace_converter(_deuter100_space, "sRGB1")
_prot50_space = {"name": "sRGB1+CVD", "cvd_type": "protanomaly", "severity": 50}
_prot50_to_sRGB1 = cspace_converter(_prot50_space, "sRGB1")
_prot100_space = {"name": "sRGB1+CVD", "cvd_type": "protanomaly", "severity": 100}
_prot100_to_sRGB1 = cspace_converter(_prot100_space, "sRGB1")


def _show_cmap(ax, rgb):
    ax.imshow(rgb[np.newaxis, ...], aspect="auto")


def _apply_rgb_mat(mat, rgb):
    return np.clip(np.einsum("...ij,...j->...i", mat, rgb), 0, 1)


# sRGB corners: a' goes from -37.4 to 45
AP_LIM = (-38, 46)
# b' goes from -46.5 to 42
BP_LIM = (-47, 43)
# J'/K goes from 0 to 100
JP_LIM = (-1, 101)


def _setup_Jpapbp_axis(ax):
    ax.set_xlabel("a' (green -> red)")
    ax.set_ylabel("b' (blue -> yellow)")
    ax.set_zlabel("J'/K (white -> black)")
    ax.set_xlim(*AP_LIM)
    ax.set_ylim(*BP_LIM)
    ax.set_zlim(*JP_LIM)


# Adapt a matplotlib colormap to a linearly transformed version -- useful for
# visualizing how colormaps look given color deficiency.
# Kinda a hack, b/c we inherit from Colormap (this is required), but then
# ignore its implementation entirely. This results in errors at runtime:
#       File "/<env>/site-packages/matplotlib/artist.py", line 1343, in format_cursor_data  # noqa: E501
#         n = self.cmap.N
#             ^^^^^^^^^^^
#     AttributeError: 'TransformedCMap' object has no attribute 'N'
class TransformedCMap(matplotlib.colors.Colormap):
    def __init__(self, transform, base_cmap):
        self.transform = transform
        self.base_cmap = base_cmap

    def __call__(self, *args, **kwargs):
        bts = kwargs.pop("bytes", False)
        fx = self.base_cmap(*args, bytes=False, **kwargs)
        tfx = self.transform(fx)
        if bts:
            return (tfx * 255).astype("uint8")
        return tfx

    def set_bad(self, *args, **kwargs):
        self.base_cmap.set_bad(*args, **kwargs)

    def set_under(self, *args, **kwargs):
        self.base_cmap.set_under(*args, **kwargs)

    def set_over(self, *args, **kwargs):
        self.base_cmap.set_over(*args, **kwargs)

    def is_gray(self):
        return False


def _vis_axes(fig):
    grid = GridSpec(
        10,
        4,
        left=0.02,
        right=0.98,
        bottom=0.02,
        width_ratios=[1] * 4,
        height_ratios=[1] * 10,
    )
    axes = {
        "cmap": grid[0, 0],
        "deltas": grid[1:4, 0],
        "cmap-greyscale": grid[0, 1],
        "lightness-deltas": grid[1:4, 1],
        "deuteranomaly": grid[4, 0],
        "deuteranopia": grid[5, 0],
        "protanomaly": grid[4, 1],
        "protanopia": grid[5, 1],
        # 'lightness': grid[4:6, 1],
        # 'colourfulness': grid[4:6, 2],
        # 'hue': grid[4:6, 3],
        "image0": grid[0:3, 2],
        "image0-cb": grid[0:3, 3],
        "image1": grid[3:6, 2],
        "image1-cb": grid[3:6, 3],
        "image2": grid[6:8, 2:],
        "image2-cb": grid[8:, 2:],
    }

    axes = {key: fig.add_subplot(value) for (key, value) in axes.items()}
    axes["gamut"] = fig.add_subplot(grid[6:, :2], projection="3d")
    return axes


def lookup_colormap_by_name(name):
    try:
        return plt.get_cmap(name)
    except ValueError:
        pass
    # Try expanding a setuptools-style entrypoint:
    #   foo.bar:baz.quux
    #   -> import foo.bar; return foo.bar.baz.quux
    if ":" in name:
        module_name, object_name = name.split(":", 1)
        object_path = object_name.split(".")
        import importlib

        cm = importlib.import_module(module_name)
        for entry in object_path:
            cm = getattr(cm, entry)
        return cm
    raise ValueError(f"Can't find colormap {name!r}")


class viscm:
    def __init__(
        self,
        cm,
        figure=None,
        uniform_space="CAM16UCS",
        name=None,
        N=256,
        N_dots=50,
        show_gamut=False,
    ):
        if isinstance(cm, str):
            cm = lookup_colormap_by_name(cm)
        if name is None:
            name = cm.name
        if figure is None:
            figure = plt.figure()
        self._sRGB1_to_uniform = lambda rgb: colour.convert(rgb, 'sRGB', uniform_space) * 100

        self.figure = figure
        self.figure.suptitle(f"Colormap evaluation: {name}", fontsize=24)

        axes = _vis_axes(self.figure)

        # ListedColormap is used for many matplotlib builtin colormaps
        # (e.g. viridis) and also what we use in the editor. It's the most
        # efficient way to work with arbitrary smooth colormaps -- pick enough
        # points that it looks smooth, and then don't waste time interpolating
        # between them. But then it creates weird issues in the analyzer if
        # our N doesn't match their N, especially when we try to compute the
        # derivative. (Specifically the derivative oscillates between 0 and a
        # large value depending on where our sample points happen to fall
        # relative to the cutoffs between the ListedColormap samples.) So if
        # this is a smooth (large N) ListedColormap, then just use its samples
        # directly:
        if isinstance(cm, ListedColormap) and cm.N >= 100:
            RGB = np.asarray(cm.colors)[:, :3]
            N = RGB.shape[0]
            x = np.linspace(0, 1, N)
        else:
            x = np.linspace(0, 1, N)
            RGB = cm(x)[:, :3]
        x_dots = np.linspace(0, 1, N_dots)
        RGB_dots = cm(x_dots)[:, :3]

        ax = axes["cmap"]
        _show_cmap(ax, RGB)
        ax.set_title("The colormap in its glory")
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        def label(ax, s):
            ax.text(
                0.95,
                0.05,
                s,
                horizontalalignment="right",
                verticalalignment="bottom",
                transform=ax.transAxes,
            )

        def title(ax, s):
            ax.text(
                0.98,
                0.98,
                s,
                horizontalalignment="right",
                verticalalignment="top",
                transform=ax.transAxes,
            )

        Jpapbp = self._sRGB1_to_uniform(RGB)

        def delta_ymax(values):
            return max(np.max(values) * 1.1, 0)

        ax = axes["deltas"]
        local_deltas = np.sqrt(np.sum((Jpapbp[:-1, :] - Jpapbp[1:, :]) ** 2, axis=-1))
        local_derivs = N * local_deltas
        ax.plot(x[1:], local_derivs)
        arclength = np.sum(local_deltas)
        rmse = np.std(local_derivs)
        title(ax, "Perceptual derivative")
        label(
            ax,
            "Length: {:0.1f}\nRMS deviation from flat: {:0.1f} ({:0.1f}%)".format(
                arclength, rmse, 100 * rmse / arclength
            ),
        )
        ax.set_ylim(-delta_ymax(-local_derivs), delta_ymax(local_derivs))
        ax.get_xaxis().set_visible(False)

        ax = axes["cmap-greyscale"]
        _show_cmap(ax, to_greyscale(RGB))
        ax.set_title("Black-and-white printed")
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = axes["lightness-deltas"]
        ax.axhline(0, linestyle="--", color="grey")
        lightness_deltas = np.diff(Jpapbp[:, 0])
        lightness_derivs = N * lightness_deltas

        ax.plot(x[1:], lightness_derivs)
        title(ax, "Perceptual lightness derivative")
        lightness_arclength = np.sum(np.abs(lightness_deltas))
        lightness_rmse = np.std(lightness_derivs)
        label(
            ax,
            "Length: {:0.1f}\nRMS deviation from flat: {:0.1f} ({:0.1f}%)".format(
                lightness_arclength,
                lightness_rmse,
                100 * lightness_rmse / lightness_arclength,
            ),
        )

        ax.set_ylim(-delta_ymax(-lightness_derivs), delta_ymax(lightness_derivs))
        ax.get_xaxis().set_visible(False)

        # ax = axes['lightness']
        # ax.plot(x, ciecam02.J)
        # label(ax, "Lightness (J)")
        # ax.set_ylim(0, 105)

        # ax = axes['colourfulness']
        # ax.plot(x, ciecam02.M)
        # label(ax, "Colourfulness (M)")

        # ax = axes['hue']
        # ax.plot(x, ciecam02.h)
        # label(ax, "Hue angle (h)")
        # ax.set_ylim(0, 360)

        def anom(ax, converter, name):
            _show_cmap(ax, np.clip(converter(RGB), 0, 1))
            label(ax, name)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

        anom(axes["deuteranomaly"], _deuter50_to_sRGB1, "Moderate deuteranomaly")
        anom(axes["deuteranopia"], _deuter100_to_sRGB1, "Complete deuteranopia")

        anom(axes["protanomaly"], _prot50_to_sRGB1, "Moderate protanomaly")
        anom(axes["protanopia"], _prot100_to_sRGB1, "Complete protanopia")

        ax = axes["gamut"]
        ax.plot(Jpapbp[:, 1], Jpapbp[:, 2], Jpapbp[:, 0])
        Jpapbp_dots = self._sRGB1_to_uniform(RGB_dots)
        ax.scatter(
            Jpapbp_dots[:, 1],
            Jpapbp_dots[:, 2],
            Jpapbp_dots[:, 0],
            c=RGB_dots[:, :],
            s=80,
        )

        # Draw a wireframe indicating the sRGB gamut
        self.gamut_patch = sRGB_gamut_patch(uniform_space)
        # That function returns a patch where each face is colored to match
        # the represented colors. For present purposes we want something
        # less... colorful.
        self.gamut_patch.set_facecolor([0.5, 0.5, 0.5, 0.1])
        self.gamut_patch.set_edgecolor([0.2, 0.2, 0.2, 0.1])
        ax.add_collection3d(self.gamut_patch)
        self.gamut_patch.set_visible(show_gamut)

        ax.view_init(elev=75, azim=-75)

        _setup_Jpapbp_axis(ax)

        images = []
        image_args = []
        example_dir = os.path.join(os.path.dirname(__file__), "viscm")

        images.append(
            np.load(os.path.join(example_dir, "st-helens_before-modified.npy")).T
        )
        image_args.append({})

        # Adapted from
        #   http://matplotlib.org/mpl_examples/images_contours_and_fields/pcolormesh_levels.py
        dx = dy = 0.05
        y, x = np.mgrid[-5 : 5 + dy : dy, -5 : 10 + dx : dx]
        z = np.sin(x) ** 10 + np.cos(10 + y * x) + np.cos(x) + 0.2 * y + 0.1 * x
        images.append(z)
        image_args.append({})

        # Peter Kovesi's colormap test image at
        #   http://peterkovesi.com/projects/colourmaps/colourmaptest.tif

        images.append(np.load(os.path.join(example_dir, "colourmaptest.npy")))

        image_args.append({})

        def _deuter_transform(RGBA):
            # clipping, alpha handling
            RGB = RGBA[..., :3]
            RGB = np.clip(_deuter50_to_sRGB1(RGB), 0, 1)
            return np.concatenate((RGB, RGBA[..., 3:]), axis=-1)

        deuter_cm = TransformedCMap(_deuter_transform, cm)

        for i, (image, args) in enumerate(zip(images, image_args)):
            ax = axes["image%i" % (i,)]
            ax.imshow(image, cmap=cm, **args)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            ax_cb = axes["image%i-cb" % (i,)]
            ax_cb.imshow(image, cmap=deuter_cm, **args)
            ax_cb.get_xaxis().set_visible(False)
            ax_cb.get_yaxis().set_visible(False)

        axes["image0"].set_title("Sample images")
        axes["image0-cb"].set_title("Moderate deuter.")
        self.axes = axes

    def toggle_gamut(self):
        self.gamut_patch.set_visible(not self.gamut_patch.get_visible())

    def save_figure(self, path):
        self.figure.savefig(path)


def sRGB_gamut_patch(uniform_space, resolution=20):
    step = 1.0 / resolution
    sRGB_quads = []
    sRGB_values = []
    # each entry in 'quads' is a 4x3 array where each row contains the
    # coordinates of a corner point
    for fixed in 0, 1:
        for i in range(resolution):
            for j in range(resolution):
                # R quad
                sRGB_quads.append(
                    [
                        [fixed, i * step, j * step],
                        [fixed, (i + 1) * step, j * step],
                        [fixed, (i + 1) * step, (j + 1) * step],
                        [fixed, i * step, (j + 1) * step],
                    ]
                )
                sRGB_values.append((fixed, (i + 0.5) * step, (j + 0.5) * step, 1))
                # G quad
                sRGB_quads.append(
                    [
                        [i * step, fixed, j * step],
                        [(i + 1) * step, fixed, j * step],
                        [(i + 1) * step, fixed, (j + 1) * step],
                        [i * step, fixed, (j + 1) * step],
                    ]
                )
                sRGB_values.append(((i + 0.5) * step, fixed, (j + 0.5) * step, 1))
                # B quad
                sRGB_quads.append(
                    [
                        [i * step, j * step, fixed],
                        [(i + 1) * step, j * step, fixed],
                        [(i + 1) * step, (j + 1) * step, fixed],
                        [i * step, (j + 1) * step, fixed],
                    ]
                )
                sRGB_values.append(((i + 0.5) * step, (j + 0.5) * step, fixed, 1))
    sRGB_quads = np.asarray(sRGB_quads)
    # work around colorspace transform bugginess in handling high-dim
    # arrays
    sRGB_quads_2d = sRGB_quads.reshape((-1, 3))
    Jpapbp_quads_2d = colour.convert(sRGB_quads_2d, "sRGB", uniform_space) * 100
    Jpapbp_quads = Jpapbp_quads_2d.reshape((-1, 4, 3))
    gamut_patch = mpl_toolkits.mplot3d.art3d.Poly3DCollection(
        Jpapbp_quads[:, :, [1, 2, 0]]
    )
    gamut_patch.set_facecolor(sRGB_values)
    gamut_patch.set_edgecolor(sRGB_values)
    return gamut_patch


def sRGB_gamut_Jp_slice(
    Jp, uniform_space, ap_lim=(-50, 50), bp_lim=(-50, 50), resolution=200
):
    bp_grid, ap_grid = np.mgrid[
        bp_lim[0] : bp_lim[1] : resolution * 1j, ap_lim[0] : ap_lim[1] : resolution * 1j
    ]
    Jp_grid = Jp * np.ones((resolution, resolution))
    Jpapbp = np.concatenate(
        (
            Jp_grid[:, :, np.newaxis],
            ap_grid[:, :, np.newaxis],
            bp_grid[:, :, np.newaxis],
        ),
        axis=2,
    )
    sRGB = colour.convert(Jpapbp, uniform_space / 100, "sRGB")
    sRGBA = np.concatenate((sRGB, np.ones(sRGB.shape[:2] + (1,))), axis=2)
    sRGBA[np.any((sRGB < 0) | (sRGB > 1), axis=-1)] = [0, 0, 0, 0]
    return sRGBA


def draw_pure_hue_angles(ax):
    # Pure hue angles from CIECAM-02
    for color, angle in [("r", 20.14), ("y", 90.00), ("g", 164.25), ("b", 237.53)]:
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        ax.plot([0, x * 1000], [0, y * 1000], color + "--")


def draw_sRGB_gamut_Jp_slice(
    ax, Jp, uniform_space, ap_lim=(-50, 50), bp_lim=(-50, 50), **kwargs
):
    sRGB = sRGB_gamut_Jp_slice(
        Jp, uniform_space, ap_lim=ap_lim, bp_lim=bp_lim, **kwargs
    )
    im = ax.imshow(sRGB, aspect="equal", extent=ap_lim + bp_lim, origin="lower")
    draw_pure_hue_angles(ax)
    ax.set_xlim(ap_lim)
    ax.set_ylim(bp_lim)
    return im
