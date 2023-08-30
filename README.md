# Roseus colormap

A perceptually uniform colormap with **full range of lightness**.


## Preview

(Colorbar image here)

(Audacity spectrogram image here)


## Motivation

The [previous version](https://github.com/dofuuz/audacity-colormap/tree/v1.0.0) of this colormap was developed for Audacity spectrogram. Roseus has now become perceptually uniform and aims to be used in a wider range of fields.

Further readings about perceptually uniform colormaps:  
https://bids.github.io/colormap/  
https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html


## The new colormap

![viscm-roseus](img/viscm-roseus.png)

Note: [viscm](https://github.com/matplotlib/viscm) used in measurements has been modified to target CAM16-UCS instead of CAM02-UCS.

Considerings while making the new colormap (in order of priority):
- Perceptually uniform
- Wide range of lightness (almost full 0-100)
- Colorful, wide range of hue, chroma
- Originality, keep magenta-ish feeling
- Pretty

![roseus-lch](img/roseus-lch.png)

![roseus-gamut](img/roseus-gamut.png)

![roseus-rgb](img/roseus-rgb.png)


## Changes from the previous version

The colormap is named 'Roseus'. (inspiration from Viridis)

Roseus now targets CAM16-UCS color space instead of the obsolute CAM02-UCS.

![viscm-audaspec](img/viscm-audaspec.png)

The previous version was perceptually smooth, but not perceptually uniform. It's now perceptually uniform.
