# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 19:18:52 2021

@author: dof
"""


import colorspacious
import matplotlib.pyplot as plt
import numpy as np

JP = 60
R = 50
TIK = 0.1

a_len = len(np.arange(-R, R, TIK))
apbp = np.mgrid[-R:R:TIK, -R:R:TIK].reshape(2, a_len, -1).T
jp = np.ones(apbp.shape[:-1]) * JP
jp = np.expand_dims(jp, 2)

Jpapbp = np.concatenate([jp, apbp], axis=2)

rgb = colorspacious.cspace_convert(Jpapbp, "CAM02-UCS", "sRGB1")
rgb[rgb<0] = 1
rgb[1<rgb] = 0

plt.imshow(rgb)
