from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Matrix:
    def __init__(self, values):
        self.values = values
        widths = set(len(line) for line in values)
        if len(widths) != 1:
            raise ValueError(f"inconsistent line sizes: {widths}")
        self.height = len(values)
        self.width = next(iter(widths))

    def __str__(self):
        return "\n".join("".join(str(c) for c in line) for line in self.values)

    def set_value_at(self, x, y, value):
        self.values[y][x] = value

    def value_at(self, x, y):
        return self.values[y][x]

    def neighbours(self, x, y):
        if x > 0:
            yield Point(x - 1, y)
        if x < self.width - 1:
            yield Point(x + 1, y)
        if y > 0:
            yield Point(x, y - 1)
        if y < self.height - 1:
            yield Point(x, y + 1)


def test_input():
    return open("input.txt")


def input():
    return open("input-2.txt")


def read_matrix(f):
    return Matrix([[int(c) for c in line.strip()] for line in f.readlines()])
