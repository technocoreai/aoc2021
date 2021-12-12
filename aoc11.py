#!/usr/bin/env python3
import utils


class CaveMap:
    def __init__(self, data):
        self.data = data.values
        self.width = data.width
        self.height = data.height

    def __str__(self):
        return "\n".join("".join(str(i) if i <= 9 else "X" for i in line) for line in self.data) + "\n"

    def check_flash(self, flashed, x, y):
        flash_count = 0
        if self.data[y][x] > 9 and (x, y) not in flashed:
            flash_count += 1
            flashed.add((x, y))
            for x2, y2 in self.sibling_coords(x, y):
                self.data[y2][x2] += 1
                flash_count += self.check_flash(flashed, x2, y2)
        return flash_count

    def sibling_coords(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if x + dx < 0 or x + dx >= self.width:
                    continue
                if y + dy < 0 or y + dy >= self.height:
                    continue
                yield x + dx, y + dy

    def step(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.data[y][x] += 1

        flash_count = 0
        flashed = set()
        for y in range(0, self.height):
            for x in range(0, self.width):
                flash_count += self.check_flash(flashed, x, y)

        if all(v > 9 for line in self.data for v in line):
            return True

        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.data[y][x] > 9:
                    self.data[y][x] = 0

        return False


def main():
    cm = CaveMap(utils.read_matrix(utils.input()))
    print(cm)
    for i in range(10000000):
        print(cm)
        if cm.step():
            print(i + 1)
            return


if __name__ == "__main__":
    main()
