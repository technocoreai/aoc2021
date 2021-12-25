#!/usr/bin/env python3
import itertools
import utils


def step(cucumbers, moved_kind, width, height):
    result = []

    busy_cells = {(x, y) for (x, y, _) in cucumbers}
    for (x, y, kind) in cucumbers:
        if kind != moved_kind:
            result.append((x, y, kind))
            continue

        if moved_kind == "v":
            new_x, new_y = (x, (y + 1) % height)
        else:
            new_x, new_y = ((x + 1) % width, y)

        if (new_x, new_y) in busy_cells:
            result.append((x, y, kind))
        else:
            result.append((new_x, new_y, kind))

    return sorted(result)


def render(cucumbers, width, height):
    result = [["."] * width for _ in range(height + 1)]
    for (x, y, kind) in cucumbers:
        result[y][x] = kind
    print("\n".join("".join(line) for line in result))
    print()


def main():
    points = [(x, y, char) for (y, line) in enumerate(utils.input()) for (x, char) in enumerate(line.strip())]
    cucumbers = sorted((x, y, kind) for (x, y, kind) in points if kind != ".")
    width, height = max((x + 1, y + 1) for x, y, _ in points)
    render(cucumbers, width, height)

    for i in itertools.count(1):
        updated = step(cucumbers, ">", width, height)
        updated = step(updated, "v", width, height)
        if updated == cucumbers:
            print(f"stopped at {i}")
            return
        cucumbers = updated
        render(cucumbers, width, height)


if __name__ == "__main__":
    main()
