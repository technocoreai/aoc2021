#!/usr/bin/env python3
import utils
from typing import NamedTuple


def segments(*coordinates):
    coordinates = sorted(coordinates)
    for c1, c2 in zip(coordinates, coordinates[1:]):
        if c1 == c2:
            continue
        yield (c1, c2)


class Cube(NamedTuple):
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def __repr__(self):
        return f"Cube({self.x1}..{self.x2}, {self.y1}..{self.y2}, {self.z1}..{self.z2})"

    @property
    def volume(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)

    def contains(self, x, y, z):
        return self.x1 <= x < self.x2 and self.y1 <= y < self.y2 and self.z1 <= z < self.z2

    def intersects(self, other):
        if other.x2 <= self.x1 or other.x1 >= self.x2:
            return False
        if other.y2 <= self.y1 or other.y1 >= self.y2:
            return False
        if other.z2 <= self.z1 or other.z1 >= self.z2:
            return False
        return True

    def subtract(self, other):
        if not self.intersects(other):
            yield self
            return
        for x1, x2 in segments(self.x1, self.x2, other.x1, other.x2):
            for y1, y2 in segments(self.y1, self.y2, other.y1, other.y2):
                for z1, z2 in segments(self.z1, self.z2, other.z1, other.z2):
                    if x1 == x2 or y1 == y2 or z1 == z2:
                        continue
                    if self.contains(x1, y1, z1) and not other.contains(x1, y1, z1):
                        yield Cube(x1, x2, y1, y2, z1, z2)


def parse(f):
    for line in f:
        action, coords = line.strip().split(" ")
        (x1, x2), (y1, y2), (z1, z2) = [tuple(int(coord) for coord in c[2:].split("..")) for c in coords.split(",")]
        yield action == "on", Cube(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1)


def turn_off(current, cube, debug=False):
    if len(current) == 0:
        return []

    result = []
    for elem in current:
        for part in elem.subtract(cube):
            result.append(part)

    return result


def turn_on(current, cube):
    pending = [cube]

    for elem in current:
        next_pending = []
        for p in pending:
            next_pending += p.subtract(elem)
        pending = next_pending

    return list(current) + pending


def main():
    turned_on = []
    for line, (action, cube) in enumerate(parse(utils.input())):
        print(f"line: {line+1}, cube: {cube}, turn on: {action}")
        turned_on = turn_on(turned_on, cube) if action else turn_off(turned_on, cube)
        print(f"total {len(turned_on)} cubes (volume {sum(c.volume for c in turned_on)})")
        print()


if __name__ == "__main__":
    main()
