#!/usr/bin/env pypy3
from functools import reduce


def siblings(cave_map, x, y):
    if x > 0:
        yield (x - 1, y)
    if x < len(cave_map[y]) - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < len(cave_map) - 1:
        yield (x, y + 1)


def find_basin(cave_map, seen_points, basin_points, x, y):
    if (x, y) in seen_points:
        return basin_points

    seen_points.add((x, y))
    if cave_map[y][x] == 9:
        return basin_points

    basin_points.add((x, y))
    for x, y in list(basin_points):
        for x1, y1 in siblings(cave_map, x, y):
            find_basin(cave_map, seen_points, basin_points, x1, y1)

    return basin_points


def main():
    total_risk = 0

    cave_map = [[int(i) for i in list(line.strip())] for line in open("/Users/zee/Downloads/input-2.txt").readlines()]

    seen_points = set()
    basins = []
    for y in range(len(cave_map)):
        for x in range(len(cave_map[0])):
            basin = find_basin(cave_map, seen_points, set(), x, y)
            if basin:
                basins.append(basin)

    result = reduce(lambda a, b: a * len(b), sorted(basins, key=len, reverse=True)[:3], 1)
    print(f"result: {result}")


if __name__ == "__main__":
    main()
