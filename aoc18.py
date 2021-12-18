#!/usr/bin/env python3
import copy
import functools
import json
import itertools
import utils
import math
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class NodePointer:
    value: object
    index: int
    level: int
    _position: Tuple[List, int]

    @property
    def is_primitive(self):
        return type(self.value) == int

    @property
    def is_regular(self):
        return type(self.value) == list and all(type(v) == int for v in self.value)

    def replace(self, new_value):
        lst, idx = self._position
        lst[idx] = new_value


def pointers(value, level=0, counter=None):
    counter = counter or itertools.count()
    for i, elem in enumerate(value):
        yield NodePointer(elem, next(counter), level + 1, (value, i))
        if type(elem) != int:
            yield from pointers(elem, level + 1, counter)


def try_explode(value):
    left_ptr = None
    exploded_ptr = None
    right_ptr = None

    for ptr in pointers(value):
        if exploded_ptr is None:
            if ptr.is_primitive:
                left_ptr = ptr
            elif ptr.level == 4 and ptr.is_regular:
                exploded_ptr = ptr
        elif ptr.index > exploded_ptr.index + 2 and ptr.is_primitive:
            right_ptr = ptr
            break

    if exploded_ptr:
        a, b = exploded_ptr.value
        if left_ptr:
            left_ptr.replace(left_ptr.value + a)
        if right_ptr:
            right_ptr.replace(right_ptr.value + b)
        exploded_ptr.replace(0)
        return True
    return False


def try_split(value):
    for ptr in pointers(value):
        if ptr.is_primitive and ptr.value >= 10:
            value = ptr.value
            ptr.replace([int(math.floor(value / 2)), int(math.ceil(value / 2))])
            return True
    return False


def sf_reduce(value):
    while True:
        if try_explode(value):
            continue
        if try_split(value):
            continue
        return


def sf_add(a, b):
    result = [copy.deepcopy(a), copy.deepcopy(b)]
    sf_reduce(result)
    return result


def magnitude(elem):
    if type(elem) == int:
        return elem
    else:
        a, b = elem
        return 3 * magnitude(a) + 2 * magnitude(b)


def main():
    numbers = [json.loads(line.strip()) for line in utils.input()]
    result = functools.reduce(sf_add, numbers)
    print(result)
    print(magnitude(result))
    magnitudes = (magnitude(sf_add(a, b)) for a, b in itertools.permutations(numbers, 2))
    print(max(magnitudes))


if __name__ == "__main__":
    main()
