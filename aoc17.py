#!/usr/bin/env python3
import utils


def sign(n):
    if n == 0:
        return 0
    elif n < 0:
        return -1
    else:
        return 1


def x_target(initial_vx, x_min, x_max):
    x = 0
    vx = initial_vx
    n = 0
    while True:
        x += vx
        vx -= sign(vx)
        n += 1

        if x_min <= x <= x_max:
            yield (initial_vx, n, vx == 0)
            if vx == 0:
                return
        elif vx == 0:
            return
        elif vx < 0 and x < x_min:
            return
        elif vx > 0 and x > x_max:
            return


def x_velocities(x_min, x_max):
    for vx in range(0, x_max + 1):
        yield from x_target(vx, x_min, x_max)


def y_targets(initial_vy, y_min, y_max):
    y = 0
    vy = initial_vy
    n = 0
    while True:
        if y_min <= y <= y_max:
            yield (initial_vy, n)
        y += vy
        vy -= 1
        n += 1
        if vy < 0 and y < y_min:
            return


def y_velocities(y_min, y_max):
    for vy in range(-1000, 1000):
        yield from y_targets(vy, y_min, y_max)


def y_pos(vy, n):
    return (n / 2) * ((2 * vy) + (n - 1) * (-1))


def valid_y_match(x_data, vy, iters):
    for _, x_iters, stopped in x_data:
        if stopped and iters >= x_iters:
            return True
        elif iters == x_iters:
            return True
    return False


def valid_velocities(x_data, y_data):
    for vx, x_iters, stopped in x_data:
        for vy, y_iters in y_data:
            if (stopped and y_iters >= x_iters) or (x_iters == y_iters):
                yield (vx, vy)


def main():
    x_min, x_max = 96, 125
    y_min, y_max = -144, -98
    x_data = [(vx, iters, stopped) for vx, iters, stopped in x_velocities(x_min, x_max)]
    print(f"x data ({len(x_data)}): {x_data}")

    y_data = [(vy, iters) for vy, iters in y_velocities(y_min, y_max)]
    print(f"y data ({len(y_data)}): {y_data}")

    max_vy = max(vy for vy, iters in y_data if valid_y_match(x_data, vy, iters))
    print(f"max vy: {max_vy}")

    highest_pos = 0 if max_vy <= 0 else y_pos(max_vy, max_vy)
    print(f"highest pos: {highest_pos}")

    print(len(set(valid_velocities(x_data, y_data))))


if __name__ == "__main__":
    main()
