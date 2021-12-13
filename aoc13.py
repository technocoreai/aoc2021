#!/usr/bin/env python3
import utils


def read_input(f):
    lines = iter(f)

    points = set()
    for line in lines:
        line = line.strip()
        if not line:
            break

        x, y = line.split(",")
        points.add((int(x), int(y)))

    folds = []
    for line in lines:
        fold_dimension, fold_line = line.replace("fold along ", "").split("=")
        folds.append((fold_dimension, int(fold_line)))

    return points, folds


def pretty_print(points):
    max_x = 0
    max_y = 0
    for x, y in points:
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    if max_x > 150 or max_y > 150:
        print(f"Board too big: {max_x}x{max_y}")
        return

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            char = "█" if ((x, y)) in points else "\x1b[2m•\x1b[0m"
            print(char, end="")
        print()


def fold(points, fold_dimension, fold_line):
    def updated(coordinate):
        return coordinate if coordinate < fold_line else fold_line - (coordinate - fold_line)

    updated_points = set()
    for x, y in points:
        if fold_dimension == "x":
            x = updated(x)
        else:
            y = updated(y)
        updated_points.add((x, y))
    return updated_points


def main():
    points, folds = read_input(utils.input())
    pretty_print(points)
    print(folds)
    print()
    for fold_dimension, fold_location in folds:
        points = fold(points, fold_dimension, fold_location)
        pretty_print(points)
        print(f"visible: {len(points)}")
        print()


if __name__ == "__main__":
    main()
