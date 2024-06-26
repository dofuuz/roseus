import numpy as np

from roseus.generator import gen_colormap
from plot_bars import CMAP_SETTINGS

HEAD = '''# Roseus colormap family
# https://github.com/dofuuz/roseus

gen_props = {}

rgb_data = [
'''

TAIL = ''']
'''


for setting, name in CMAP_SETTINGS:
    color_data, _ = gen_colormap(*setting)

    with open(f'roseus/cmap/{name}.py', 'w') as f:
        f.write(HEAD.format(setting))
        for r, g, b in color_data:
            f.write(f'    [{r:.6f}, {g:.6f}, {b:.6f}],\n')
        f.write(TAIL)

    np.save(f'roseus/cmap/{name}.npy', color_data.astype(np.float32))


with open(f'roseus/cmap/__init__.py', 'w') as f:
    f.write('cmap_names = {\n')
    for _, name in CMAP_SETTINGS:
        f.write(f"    '{name}',\n")
    f.write('}\n')


with open(f'roseus/mpl.pyi', 'w') as f:
    f.write('from matplotlib.colors import ListedColormap\n\n')
    for _, name in CMAP_SETTINGS:
        f.write(f'{name}: ListedColormap\n')
        f.write(f'{name}_r: ListedColormap\n')
