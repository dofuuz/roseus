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
    with open(f'roseus/cmap/{name}.py', 'w') as f:
        color_data, _ = gen_colormap(*setting)

        f.write(HEAD.format(setting))
        for r, g, b in color_data:
            f.write(f'    [{r:.6f}, {g:.6f}, {b:.6f}],\n')
        f.write(TAIL)
