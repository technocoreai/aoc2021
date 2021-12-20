#!/usr/bin/env python3
from typing import Tuple, Set
import math
import utils
from dataclasses import dataclass


@dataclass
class Image:
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    lit_pixels: Set[Tuple[int, int]]
    default_lit: bool

    def pixel_lit(self, x, y):
        if self.default_lit:
            return (x, y) not in self.lit_pixels
        else:
            return (x, y) in self.lit_pixels

    def pixel_count(self):
        if self.default_lit:
            return math.inf
        else:
            return len(self.lit_pixels)


def parse(f):
    algo, input = f.read().split("\n\n")
    algo = set(i for i, c in enumerate("".join(l.strip() for l in algo)) if c == "#")
    input_lines = [line.strip() for line in input.strip().split("\n")]
    input_pixels = set((x, y) for y, line in enumerate(input_lines) for x, v in enumerate(line) if v == "#")
    return algo, Image(0, 0, len(input_lines[0]) - 1, len(input_lines) - 1, input_pixels, default_lit=False)


def position_for(image, x, y):
    result = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            result <<= 1
            if image.pixel_lit(x + dx, y + dy):
                result |= 1
    return result


def enhance(algo, image):
    default_position = 511 if image.default_lit else 0
    default_lit = default_position in algo

    result = set()
    for x in range(image.min_x - 1, image.max_x + 2):
        for y in range(image.min_y - 1, image.max_y + 2):
            pixel_lit = position_for(image, x, y) in algo
            if pixel_lit != default_lit:
                result.add((x, y))

    return Image(image.min_x - 1, image.min_y - 1, image.max_x + 1, image.max_y + 1, result, default_lit)


def main():
    algo, image = parse(utils.input())
    print(image.pixel_count())
    for _ in range(50):
        image = enhance(algo, image)
        print(image.pixel_count())


if __name__ == "__main__":
    main()
