from collections import namedtuple
from random import randint
from math import sqrt

cell_mapper = {
    '#': float('inf'),
    '~': 800,
    '*': 200,
    '+': 150,
    'X': 120,
    '_': 100,
    'H': 70,
    'T': 50
}

dataset = open("1_victoria_lake.txt", 'r')
N, M, C, R = tuple(map(int, dataset.readline().split(' ')))
customers = [tuple(map(int, dataset.readline().split(' '))) for _ in range(C)]
problem_map = [row[:-1] for row in dataset]

K = C//R
L = 150
EPSILON = 6
MAX_FAILS = 10
MIN_WEIGHT = -1000


def random_path(x1, y1, x2, y2):
    pos_x, pos_y = x1, y1
    path = ""
    weight = 0
    fails = 0

    while (not (pos_x == x2 and pos_y == y2)) and fails < MAX_FAILS:
        Pu = max(0, (pos_y - y2)**3 + EPSILON)
        Pd = max(0, (y2 - pos_y)**3 + EPSILON)
        Pr = max(0, (x2 - pos_x)**3 + EPSILON)
        Pl = max(0, (pos_x - x2)**3 + EPSILON)

        choice = randint(0, Pu + Pd + Pr + Pl)

        if choice <= Pu:
            if problem_map[pos_y-1][pos_x] == '#':
                fails += 1
                continue
            path += 'U'
            pos_y -= 1
            fails = 0
        elif choice <= Pu + Pd:
            if problem_map[pos_y+1][pos_x] == '#':
                fails += 1
                continue
            path += 'D'
            pos_y += 1
            fails = 0
        elif choice <= Pu + Pd + Pr:
            if problem_map[pos_y][pos_x+1] == '#':
                fails += 1
                continue
            path += 'R'
            pos_x += 1
            fails = 0
        else: # if choice <= Pu + Pd + Pr + Pl:
            if problem_map[pos_y][pos_x-1] == '#':
                fails += 1
                continue
            path += 'L'
            pos_x -= 1
            fails = 0

        weight += cell_mapper[problem_map[pos_y][pos_x]]

    if fails < MAX_FAILS:
        return (path, weight)
    else:
        return (None, -1)



def new_solution():
    connected = [False]*C
    POINTS = 0
    paths = []
    r = 0

    while r < R:
        x = randint(0, N-1)
        y = randint(0, M-1)

        skip = False
        if problem_map[y][x] == '#':
            skip = True
        for c in customers:
            if x == c[0] and y == c[1]:
                skip = True
                break
        for _x, _y, _p in paths:
            if _x == x and _y == y:
                skip = True
                break
        if skip:
            continue

        # print("\nR:", x, y)

        distances = [(i, sqrt((y-c[0])**2 + (x-c[1])**2)) for i, c in enumerate(customers)]
        distances.sort(key=lambda x: x[1])

        for i, d in distances[:K]:
            c = customers[i]

            best_path, best_w = None, float('inf')
            for l in range(L):
                try:
                    p, w = random_path(x, y, c[0], c[1])
                except:
                    p, w = None, -1

                if w < best_w and w != -1:
                    best_w = w
                    best_path = p

            # print("Best w:", best_w, "Path:", best_path)
            points = customers[i][2] - best_w
            # print("  C:", c[0], c[1], " --> ", best_path, "=", best_w)

            if points > MIN_WEIGHT and best_path != None:
                # print("   ", points, " => ", best_path)
                POINTS += points
                paths.append((x, y, best_path))
                connected[i] = True
            # else:
                # print("    No path found")

        r += 1

    all_connected = True
    bonus = 0
    for i in range(C):
        if not connected[i]:
            all_connected = False
            break
        else:
            bonus += customers[i][2]

    total = POINTS if not all_connected else POINTS + bonus
    return (paths, total)





MAX_POINTS = 0
best_solution = None

try:
    while True:
        paths, total = new_solution()

        if total > MAX_POINTS:
            MAX_POINTS = total
            best_solution = paths
            print("New best:", total)

            out = open("sol_" + str(total) + ".txt", 'w')
            for x, y, p in paths:
                out.write("{} {} {}\n".format(x, y, p))
            out.close()
            # print("\n\n-------\nPoints:", POINTS)
            # print("    Paths:", paths)
            # print("    All connected:", all_connected)
            # print("    Possible bonus:", bonus)
            # print("---------\nTOTAL:", POINTS if not all_connected else POINTS + bonus)
        else:
            K = C//R + randint(0, 3)
            L = 50 + randint(0, 300)
            EPSILON = randint(1, 8)
            MAX_FAILS = randint(3, 20)
            MIN_WEIGHT = randint(-3000, 0)
except KeyboardInterrupt:
    print(paths)
