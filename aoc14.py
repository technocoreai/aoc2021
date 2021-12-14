#!/usr/bin/env python3
import functools
from collections import Counter
import utils


def parse_input(f):
    i = (l.strip() for l in iter(f))

    initial = next(i)
    next(i)

    rules = {}
    for line in i:
        pair, insertion = line.split(" -> ")
        rules[tuple(pair)] = insertion

    return initial, rules


def polymerizer_for(rules):
    @functools.lru_cache(10240)
    def polymerize_inner(a, b, n):
        if n == 0:
            return Counter([a, b])
        else:
            insertion = rules[(a, b)]
            result = Counter({insertion: -1})
            result += polymerize_inner(a, insertion, n - 1)
            result += polymerize_inner(insertion, b, n - 1)
            return result

    return polymerize_inner


def main():
    current, rules = parse_input(utils.input())
    polymerizer = polymerizer_for(rules)
    iterations = 40

    totals = Counter(current[0])
    for a, b in zip(current, current[1:]):
        totals += polymerizer(a, b, iterations)
        totals[a] -= 1
    print(totals)
    print(max(totals.values()) - min(totals.values()))


if __name__ == "__main__":
    main()
