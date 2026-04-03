import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
import numpy as np


def solve(variables, domains, neighbors):
    def is_consistent(var, val, assignment):
        return all(assignment.get(n) != val for n in neighbors.get(var, []))

    def forward_check(var, val, assignment):
        removed = {}
        for n in neighbors.get(var, []):
            if n not in assignment:
                removed[n] = [v for v in domains[n] if v == val]
                for v in removed[n]:
                    domains[n].remove(v)
                if not domains[n]:
                    for k, vs in removed.items():
                        domains[k].extend(vs)
                    return None
        return removed

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        var = min((v for v in variables if v not in assignment), key=lambda v: len(domains[v]))
        for val in list(domains[var]):
            if is_consistent(var, val, assignment):
                assignment[var] = val
                removed = forward_check(var, val, assignment)
                if removed is not None:
                    result = backtrack(assignment)
                    if result:
                        return result
                del assignment[var]
                if removed:
                    for k, vs in removed.items():
                        domains[k].extend(vs)
        return None

    return backtrack({})


neighbors = {
    'Adilabad':                  ['Kumurambheem Asifabad', 'Nirmal', 'Mancherial'],
    'Kumurambheem Asifabad':     ['Adilabad', 'Mancherial'],
    'Mancherial':                ['Adilabad', 'Kumurambheem Asifabad', 'Jagtial', 'Peddapalli', 'Nirmal'],
    'Nirmal':                    ['Adilabad', 'Mancherial', 'Nizamabad', 'Kamareddy', 'Jagtial'],
    'Nizamabad':                 ['Nirmal', 'Kamareddy', 'Medak', 'Siddipet', 'Rajanna Sircilla', 'Jagtial'],
    'Jagtial':                   ['Nirmal', 'Mancherial', 'Nizamabad', 'Karimnagar', 'Peddapalli', 'Rajanna Sircilla'],
    'Peddapalli':                ['Mancherial', 'Jagtial', 'Karimnagar', 'Jayashankar Bhupalpally', 'Mulugu'],
    'Karimnagar':                ['Jagtial', 'Peddapalli', 'Rajanna Sircilla', 'Siddipet', 'Jayashankar Bhupalpally'],
    'Rajanna Sircilla':          ['Nizamabad', 'Jagtial', 'Karimnagar', 'Siddipet'],
    'Kamareddy':                 ['Nirmal', 'Nizamabad', 'Medak', 'Sangareddy'],
    'Mulugu':                    ['Peddapalli', 'Jayashankar Bhupalpally', 'Mahabubabad', 'Bhadradri Kothagudem', 'Hanamkonda'],
    'Jayashankar Bhupalpally':   ['Peddapalli', 'Karimnagar', 'Mulugu', 'Hanamkonda', 'Siddipet'],
    'Medak':                     ['Kamareddy', 'Nizamabad', 'Sangareddy', 'Siddipet', 'Medchal Malkajgiri'],
    'Siddipet':                  ['Nizamabad', 'Rajanna Sircilla', 'Karimnagar', 'Jayashankar Bhupalpally', 'Medak', 'Sangareddy', 'Yadadri Bhongir', 'Jangaon'],
    'Jangaon':                   ['Siddipet', 'Hanamkonda', 'Yadadri Bhongir', 'Medchal Malkajgiri'],
    'Hanamkonda':                ['Jayashankar Bhupalpally', 'Mulugu', 'Mahabubabad', 'Jangaon', 'Siddipet'],
    'Mahabubabad':               ['Hanamkonda', 'Mulugu', 'Bhadradri Kothagudem', 'Khammam', 'Suryapet', 'Jangaon'],
    'Bhadradri Kothagudem':      ['Mulugu', 'Mahabubabad', 'Khammam'],
    'Khammam':                   ['Bhadradri Kothagudem', 'Mahabubabad', 'Suryapet', 'Nalgonda'],
    'Rangareddy':                ['Vikarabad', 'Hyderabad', 'Medchal Malkajgiri', 'Yadadri Bhongir', 'Mahabubnagar', 'Nagarkurnool', 'Nalgonda'],
    'Hyderabad':                 ['Rangareddy', 'Medchal Malkajgiri', 'Sangareddy'],
    'Medchal Malkajgiri':        ['Medak', 'Sangareddy', 'Hyderabad', 'Rangareddy', 'Jangaon', 'Yadadri Bhongir'],
    'Yadadri Bhongir':           ['Medchal Malkajgiri', 'Jangaon', 'Siddipet', 'Rangareddy', 'Nalgonda', 'Suryapet'],
    'Suryapet':                  ['Yadadri Bhongir', 'Mahabubabad', 'Khammam', 'Nalgonda'],
    'Nalgonda':                  ['Yadadri Bhongir', 'Suryapet', 'Khammam', 'Rangareddy', 'Mahabubnagar', 'Nagarkurnool'],
    'Mahabubnagar':              ['Rangareddy', 'Nalgonda', 'Nagarkurnool', 'Wanaparthy', 'Narayanpet'],
    'Narayanpet':                ['Mahabubnagar', 'Wanaparthy', 'Jogulamba Gadwal'],
    'Jogulamba Gadwal':          ['Narayanpet', 'Wanaparthy', 'Nagarkurnool'],
    'Wanaparthy':                ['Mahabubnagar', 'Narayanpet', 'Jogulamba Gadwal', 'Nagarkurnool'],
    'Nagarkurnool':              ['Mahabubnagar', 'Nalgonda', 'Rangareddy', 'Wanaparthy', 'Jogulamba Gadwal'],
    'Vikarabad':                 ['Rangareddy', 'Sangareddy'],
    'Sangareddy':                ['Kamareddy', 'Medak', 'Vikarabad', 'Hyderabad', 'Medchal Malkajgiri'],
}

color_names = ['#E74C3C', '#2ECC71', '#3498DB', '#F39C12', '#9B59B6']
solution = solve(list(neighbors.keys()), {v: list(color_names) for v in neighbors}, neighbors)

with open("telangana_district.geojson") as f:
    geojson = json.load(f)

fig, ax = plt.subplots(1, 1, figsize=(14, 12))
ax.set_facecolor('#F0F4F8')
fig.patch.set_facecolor('#F0F4F8')

for feature in geojson['features']:
    name = feature['properties']['district']
    coords = feature['geometry']['coordinates'][0]
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    color = solution.get(name, '#CCCCCC')
    ax.fill(xs, ys, color=color, edgecolor='white', linewidth=1.5, zorder=2)
    cx = sum(xs[:-1]) / (len(xs) - 1)
    cy = sum(ys[:-1]) / (len(ys) - 1)
    short = name if len(name) <= 12 else name[:10] + '..'
    ax.text(cx, cy, short, ha='center', va='center', fontsize=5.5,
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.1', facecolor='none', edgecolor='none'),
            zorder=3)

legend_labels = {
    '#E74C3C': 'Color 1', '#2ECC71': 'Color 2',
    '#3498DB': 'Color 3', '#F39C12': 'Color 4', '#9B59B6': 'Color 5'
}
patches = [mpatches.Patch(color=c, label=l) for c, l in legend_labels.items()]
ax.legend(handles=patches, loc='lower left', fontsize=9, framealpha=0.9)

ax.set_title('Telangana Districts — CSP Map Coloring', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Longitude', fontsize=10)
ax.set_ylabel('Latitude', fontsize=10)
ax.grid(True, alpha=0.3, zorder=1)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('telangana_map_output.png', dpi=150, bbox_inches='tight')
print("Saved telangana_map_output.png")
