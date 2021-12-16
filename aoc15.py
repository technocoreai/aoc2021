#!/usr/bin/env python3
import sortedcontainers
import math
import utils


def find_path(cave):
    candidates = sortedcontainers.SortedSet()
    scores = {utils.Point(x, y): math.inf for x in range(cave.width) for y in range(cave.height)}
    current_node = utils.Point(0, 0)
    scores[current_node] = 0
    target_node = (cave.width - 1, cave.height - 1)

    while True:
        current_score = scores[current_node]
        print(f"{current_node}, {current_score}, {len(candidates)}")

        for neighbour in cave.neighbours(current_node.x, current_node.y):
            new_value = current_score + cave.value_at(neighbour.x, neighbour.y)

            current_value = scores[neighbour]
            if new_value < current_value:
                scores[neighbour] = new_value
                candidates.add(neighbour)

        if len(candidates) == 0:
            return scores[target_node]
        else:
            current_node = candidates.pop(0)


def expand(cave):
    new_cave = utils.Matrix([[0] * cave.width * 5 for y in range(cave.height * 5)])
    for y in range(cave.width):
        for x in range(cave.height):
            new_cave.set_value_at(x, y, cave.value_at(x, y))

    for i in range(1, 5):
        for y in range(cave.height):
            for x in range(cave.width):
                new_value = new_cave.value_at(x + cave.width * (i - 1), y) + 1
                if new_value > 9:
                    new_value = 1
                new_cave.set_value_at(x + cave.width * i, y, new_value)
    for i in range(1, 5):
        for y in range(cave.height):
            for x in range(new_cave.width):
                new_value = new_cave.value_at(x, y + cave.height * (i - 1)) + 1
                if new_value > 9:
                    new_value = 1
                new_cave.set_value_at(x, y + cave.height * i, new_value)

    return new_cave


def main():
    cave = utils.read_matrix(utils.input())
    expanded = expand(cave)
    print(find_path(expanded))


if __name__ == "__main__":
    main()
