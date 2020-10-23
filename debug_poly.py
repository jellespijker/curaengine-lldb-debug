import sys
import ast
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.pyplot import cm

def pplot(**kwargs):
    plt.figure(figsize=(12, 12))
    plt.axis('equal')
    for k, v in kwargs.items():
        plt.fill(v[:, 0], v[:, 1], label=k, alpha=1/len(kwargs))
    plt.legend()
    plt.show()

def buildpath(poly):
    poly = np.append(poly, np.array([poly[0]]), axis=0)
    codes = [Path.LINETO for c in range(len(poly))]
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY
    return Path(poly, codes)

def pathplot(**kwargs):
    fig, ax = plt.subplots()
    plt.axis('equal')
    bounds_y = [sys.maxsize, 0]
    bounds_x = [sys.maxsize, 0]
    nopoly = sum([len(p) for p in kwargs.values()])
    colors = cm.rainbow(np.linspace(0, 1, nopoly))
    c_idx = 0
    for k, p in kwargs.items():
        idx = 0
        for v in p:
            bounds_x[0] = min(v[:, 0]) if min(v[:, 0]) < bounds_x[0] else bounds_x[0]
            bounds_x[1] = max(v[:, 0]) if max(v[:, 0]) > bounds_x[1] else bounds_x[1]
            bounds_y[0] = min(v[:, 1]) if min(v[:, 0]) < bounds_y[0] else bounds_y[0]
            bounds_y[1] = max(v[:, 1]) if max(v[:, 0]) > bounds_y[1] else bounds_y[1]
            path = buildpath(v)
            patch = patches.PathPatch(path, edgecolor=colors[c_idx], facecolor='None', alpha=1/len(kwargs), linewidth=2, label="{}_{}".format(k, idx))
            ax.add_patch(patch)
            idx += 1
            c_idx += 1
    bounds_x[0] -= 100
    bounds_x[1] += 100
    bounds_y[0] -= 100
    bounds_y[1] += 100
    ax.set_xlim(*bounds_x)
    ax.set_ylim(*bounds_y)
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    polygons = {}
    for line in sys.stdin:
        key, value = line.split(" = {cura::Polygons} ")
        polygons[key] = []
        parsed = ast.literal_eval(value)
        for poly in parsed:
            polygons[key].append(np.array(poly))
    print(polygons)
    pathplot(**polygons)
