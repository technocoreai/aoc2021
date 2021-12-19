#!/usr/bin/env python3
import itertools
import utils
from typing import NamedTuple, Set

SIMILARITY_FACTOR = 12


class Position(NamedTuple):
    x: int
    y: int
    z: int

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return str(self)

    def change_facing(self, n):
        if n == 0:
            return self
        elif n == 1:
            return Position()

    def with_scanner_facing(self, n):
        if n == 0:
            return self
        elif n == 1:
            return Position(x=self.x, y=-self.y, z=-self.z)
        elif n == 2:
            return Position(x=self.y, y=-self.x, z=self.z)
        elif n == 3:
            return Position(x=-self.y, y=self.x, z=self.z)
        elif n == 4:
            return Position(x=self.x, y=self.z, z=-self.y)
        elif n == 5:
            return Position(x=self.x, y=-self.z, z=self.y)
        else:
            raise ValueError(f"bad facing: {n}")

    def with_scanner_rotation(self, n):
        if n == 0:
            return self
        elif n == 1:
            return Position(x=self.z, y=self.y, z=-self.x)
        elif n == 2:
            return Position(x=-self.x, y=self.y, z=-self.z)
        elif n == 3:
            return Position(x=-self.z, y=self.y, z=self.x)
        else:
            raise ValueError(f"bad rotation: {n}")

    def translate(self, dx, dy, dz):
        return Position(x=self.x + dx, y=self.y + dy, z=self.z + dz)

    def distance(self, p2):
        return abs(p2.x - self.x) + abs(p2.y - self.y) + abs(p2.z - self.z)


class Scanner(NamedTuple):
    id: int
    beacons: Set[Position]


def orientations(beacons):
    for f in range(6):
        for r in range(4):
            yield [p.with_scanner_facing(f).with_scanner_rotation(r) for p in beacons]


def try_merge(existing_beacons, beacons):
    for orientation in orientations(beacons):
        for existing_beacon in existing_beacons:
            for candidate_beacon in orientation:
                dx = existing_beacon.x - candidate_beacon.x
                dy = existing_beacon.y - candidate_beacon.y
                dz = existing_beacon.z - candidate_beacon.z

                total = 0
                for point in orientation:
                    if not point.translate(dx, dy, dz) in existing_beacons:
                        continue

                    total += 1
                    if total >= SIMILARITY_FACTOR:
                        result = existing_beacons.copy()
                        result.update(p.translate(dx, dy, dz) for p in orientation)
                        return result, Position(dx, dy, dz)
    return None, None


def parse(f):
    scanner_id = None
    beacons = set()
    for line in f:
        line = line.strip()
        if "---" in line:
            if beacons:
                yield Scanner(scanner_id, set(beacons))
            scanner_id = int(line.replace("--- scanner ", "").replace("---", ""))
            beacons = set()
        elif line:
            x, y, z = line.split(",")
            beacons.add(Position(int(x), int(y), int(z)))
    if beacons:
        yield Scanner(scanner_id, set(beacons))


def main():
    scanners = list(parse(utils.input()))
    current_beacons = scanners.pop(0).beacons
    scanner_positions = [Position(0, 0, 0)]
    while scanners:
        candidate = scanners.pop(0)
        updated_beacons, scanner_position = try_merge(current_beacons, candidate.beacons)
        if updated_beacons:
            current_beacons = updated_beacons
            scanner_positions.append(scanner_position)
            print(f"merged {candidate.id} (scanner at {scanner_position})", end=", ")
        else:
            scanners.append(candidate)
            print(f"failed to merge {candidate.id}", end=", ")
        print(f"{len(scanners)} remaining, {len(current_beacons)} points known")

    max_distance = max(p1.distance(p2) for p1, p2 in itertools.combinations(scanner_positions, 2))
    print(f"max scanner distance: {max_distance}")


if __name__ == "__main__":
    main()
