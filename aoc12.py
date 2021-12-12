#!/usr/bin/env python3
from collections import defaultdict
import utils


def paths(
    edges,
    visit_small_twice_target,
    current_node="start",
    current_path=tuple(),
    visited={"start": 2},
):
    current_path += (current_node,)

    if current_node == "end":
        yield current_path
        return
    else:
        if current_node.islower():
            visited = visited.copy()
            visited[current_node] = visited.get(current_node, 0) + (
                1 if current_node == visit_small_twice_target else 2
            )
        for next_node in edges[current_node]:
            if visited.get(next_node, 0) < 2:
                yield from paths(
                    edges, visit_small_twice_target, current_node=next_node, current_path=current_path, visited=visited
                )


def parse_edges(f):
    edges = defaultdict(set)
    for line in f:
        line = line.strip().split("-")
        edges[line[0]].add(line[1])
        edges[line[1]].add(line[0])
    return edges


def find_paths(edges):
    seen = set()
    for node in edges:
        if node not in ("start", "end") and node.islower():
            for path in paths(edges, visit_small_twice_target=node):
                if path not in seen:
                    seen.add(path)
                    yield path


def main():
    edges = parse_edges(utils.input())
    for path in find_paths(edges):
        print(path)


if __name__ == "__main__":
    main()
