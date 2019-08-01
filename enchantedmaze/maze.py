# https://www.redblobgames.com/grids/hexagons/

import collections
import csv

EvenQ = collections.namedtuple('EvenQ', ['q', 'r'])
Cube = collections.namedtuple('Cube', ['x', 'y', 'z'])

def evenq_to_cube(hex):
    x = hex.q
    z = hex.r - (hex.q + (hex.q & 1)) // 2
    y = 0 - x - z
    return Cube(x, y, z)

cube_directions = [
    Cube( 0, +1, -1), # N
    Cube(+1,  0, -1), # NE
    Cube(+1, -1,  0), # SE
    Cube( 0, -1, +1), # S
    Cube(-1,  0, +1), # SW
    Cube(-1, +1,  0)  # NW
]

elems = dict()
elems_cube = dict()
with open('maze.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for r, row in enumerate(reader):
        for q, elem in enumerate(row):
            eq = EvenQ(q, r)
            cube = evenq_to_cube(eq)
            if elem != '':
                elems[eq] = elem
                elems_cube[cube] = elem
print(elems)
print(elems_cube)

for r in range(7):
    for q in range(1,6,2): # odds up
        c = EvenQ(q, r)
        print("  ", end="")
        if c in elems:
            print(elems[c]+" ", end="")
        else:
            print("# ", end="")
    print()
    for q in range(0,6,2): # evens down
        c = EvenQ(q, r)
        if c in elems:
            print(elems[c]+" ", end="")
        else:
            print("# ", end="")
        print("  ", end="")
    print()

