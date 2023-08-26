from audaspec2 import gen_colormap


HEAD = '''# Roseus colormap data
# https://github.com/dofuuz/audacity-colormap

roseus_data = [
'''

TAIL = ''']

if __name__ == '__main__':
    from matplotlib.colors import ListedColormap
    import matplotlib.pyplot as plt
    import numpy as np

    auda_cm = ListedColormap(roseus_data, name='Roseus')
    plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=auda_cm)
    plt.show()
'''


with open('generated/colormap_dof.py', 'w') as f:
    color_data, _ = gen_colormap()

    f.write(HEAD)
    for r, g, b in color_data:
        f.write(f'    [{r:.6f}, {g:.6f}, {b:.6f}],\n')
    f.write(TAIL)
