# coding=utf-8
import sys
import math


MAX_ITER = 1000000000


class Ride(object):
    def __init__(self, i, line):
        a, b, x, y, s, f = tuple(map(int, line.split(' ')))
        self.id = i
        self.start_position = (a, b)
        self.finish_position = (x, y)
        self.start_time = s
        self.finish_time = f
        self.time = distance(self.start_position, self.finish_position)

    def __str__(self):
        f = 'Id: {}, StartPos: {}, StartTime: {}, FinishPos: {}, FinishTime: {}'  # noqa
        return f.format(self.id, self.start_position, self.start_time, self.finish_position, self.finish_time)  # noqa


class Car(object):
    def __init__(self, i):
        self.id = i
        self.time = 0
        self.rides = []

    def add_ride(self, ride, offset):
        self.rides.append(ride)
        self.time += offset + ride.time

    def last_ride(self):
        return self.rides[-1] if len(self.rides) > 0 else None

    def solution(self):
        return '{} {}\n'.format(len(self.rides), ' '.join([str(ride.id) for ride in self.rides]))  # noqa


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# t è il tempo quando siamo già arrivati a tratta1.finish_position
def coefficent(tratta1, tratta2, t):
    d = distance(tratta1.finish_position, tratta2.start_position)
    if d + tratta2.time + t > tratta2.finish_time:
        return 2 ** 32
    offset = tratta2.start_time - (t + d)
    if offset < 0:
        offset = 0
    return d + offset


def start_coefficent(tratta):
    d = distance((0, 0), tratta.start_position)
    offset = tratta.start_time - d
    if offset < 0:
        offset = 0
    return d + offset


def read_file(f):
    f = open(f)
    params = tuple(map(int, f.readline().split(' ')))
    rides = [Ride(i, line) for i, line in enumerate(f)]
    f.close()
    return params, rides


def best_one(last_ride, rides, t):
    best_ride, best_offset = -1, -1
    for i, ride in enumerate(rides):
        tmp = coefficent(last_ride, ride, t)
        if (tmp < best_offset or best_offset == -1):
            best_ride = i
            best_offset = tmp
    return rides.pop(best_ride), best_offset


def try_to_solve(params, rides, output_filename):
    global MAX_ITER
    rides = sorted(rides, key=start_coefficent)
    R, C, F, N, B, T = params
    cars = [Car(i) for i in range(F)]

    # La prima migliore
    for car in cars:
        ride = rides.pop(0)
        car.add_ride(ride, start_coefficent(ride))

    couter = 0
    while(len(rides) > 0 and couter < MAX_ITER):
        # Le prossima scelta
        for car in cars:
            if len(rides) > 0:
                last = car.last_ride()
                if last is not None:
                    best, offset = best_one(last, rides, car.time)
                    car.add_ride(best, offset)
                else:
                    best = rides.pop(0)
                    offset = start_coefficent(best)
                    car.add_ride(best, offset)
        couter += 1

    out = open(output_filename, 'w')
    for car in cars:
        out.write(car.solution())
    out.close()


if __name__ == '__main__':
    file_name = sys.argv[1]
    output_filename = 'output/{}.out'.format(file_name.split(".")[0].split("/")[1])  # noqa
    params, rides = read_file(file_name)
    try_to_solve(params, rides, output_filename)
