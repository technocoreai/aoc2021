#!/usr/bin/env python3
import sqlite3
import utils
import time


def execute(cursor, tokens, debug=False):
    cmd = tokens[0]
    op1 = tokens[1]
    if cmd == "inp":
        sub_vars = ["?" if var == op1 else var for var in ("x", "y", "z", "w")]

        for i in range(1, 10):
            cursor.execute(
                f"""
                insert into states(x, y, z, w, num)
                select {', '.join(sub_vars)}, num * 10 + ?
                  from old_states
            """,
                (i, i),
            )
    else:
        op2 = tokens[2]
        if cmd == "add":
            expr = f"{op1} + {op2}"
        elif cmd == "mul":
            expr = f"{op1} * {op2}"
        elif cmd == "div":
            expr = f"{op1} / {op2}"
        elif cmd == "mod":
            expr = f"{op1} % {op2}"
        elif cmd == "eql":
            expr = f"case when {op1} == {op2} then 1 else 0 end"

        sub_vars = [f"{expr} as {var}" if var == op1 else f"{var} as {var}" for var in ("x", "y", "z", "w")]

        cursor.execute(
            f"""
            insert into states(x, y, z, w, num)
            select x as x, y as y, z as z, w as w, min(num) as num from (
                select {', '.join(sub_vars)}, num
                  from old_states
            ) group by x, y, z, w
        """
        )


def main():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("create table states(x int, y int, z int, w int, num int)")
    cursor.execute("insert into states (x, y, z, w, num) values (0, 0, 0, 0, 0)")

    for idx, line in enumerate(utils.test_input()):
        line = line.strip()
        print(f"[{idx+1}]: {line}")
        cursor.execute("drop table if exists old_states")
        cursor.execute("alter table states rename to old_states")
        cursor.execute("create table states(x int, y int, z int, w int, num int)")

        start = time.time()
        execute(cursor, line.split(" "), debug=True)
        end = time.time()

        if False:
            cursor.execute("select x, y, z, w, num from states")
            for x, y, z, w, num in cursor:
                print(f" x: {x}, y: {y}, z: {z}, w: {w} / {num}")

        cursor.execute("select max(_rowid_) from states limit 1")
        (states,) = cursor.fetchone()
        print(f"{states} states, {time.time() - start:.02f} seconds")
        print()

    cursor.execute("select min(num) from states where z = 0")
    (answer,) = cursor.fetchone()
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
