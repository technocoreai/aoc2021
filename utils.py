class Matrix:
    def __init__(self, values):
        self.values = values
        widths = set(len(line) for line in values)
        if len(widths) != 1:
            raise ValueError(f"inconsistent line sizes: {widths}")
        self.height = len(values)
        self.width = next(iter(widths))


def test_input():
    return open("input.txt")


def input():
    return open("input-2.txt")


def read_matrix(f):
    return Matrix([[int(c) for c in line.strip()] for line in f.readlines()])
