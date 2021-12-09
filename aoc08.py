#!/usr/bin/env pypy3
import copy
from collections import Counter
import itertools

WIRES = ["a", "b", "c", "d", "e", "f", "g"]

DIGITS = {
    "0": frozenset("abcefg"),
    "1": frozenset("cf"),
    "2": frozenset("acdeg"),
    "3": frozenset("acdfg"),
    "4": frozenset("bcdf"),
    "5": frozenset("abdfg"),
    "6": frozenset("abdefg"),
    "7": frozenset("acf"),
    "8": frozenset("abcdefg"),
    "9": frozenset("abcdfg"),
}

REVERSE_DIGITS = {v: k for k, v in DIGITS.items()}


LENGTHS = Counter(len(x) for x in DIGITS.values())


def updated_mappings(current_mappings, updates):
    next_mappings = current_mappings.copy()
    for src, tgt in updates:
        existing = next_mappings.get(src)
        if existing == tgt or existing is None:
            next_mappings[src] = tgt
        else:
            raise ValueError(f"{src}: {tgt} != {existing}")
    return next_mappings


def solutions_inner(remaining_input, current_mappings):
    if len(remaining_input) == 0:
        yield current_mappings
        return

    current_digit = remaining_input[0]
    for word in DIGITS.values():
        if len(word) != len(current_digit):
            continue

        for perm in itertools.permutations(word):
            try:
                next_mappings = updated_mappings(current_mappings, zip(current_digit, perm))
            except ValueError as e:
                continue
            else:
                yield from solutions_inner(remaining_input[1:], next_mappings)


def solutions(line):
    yield from solutions_inner(sorted(line, key=lambda x: LENGTHS[len(x)]), {})


def solve_line(line):
    input, output = line.split(" | ")
    input = input.split(" ")
    output = output.split(" ")
    combined = input + output
    for mapping in solutions(combined):
        return int("".join(REVERSE_DIGITS[frozenset(mapping[c] for c in word)] for word in output))


def main():
    result = 0
    with open("/Users/zee/Downloads/input.txt") as f:
        for line in f:
            line = line.strip()
            output = solve_line(line)
            print(output)
            result += output
    print(f"total: {result}")


if __name__ == "__main__":
    main()
