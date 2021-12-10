#!/usr/bin/env python3

PAREN_MAP = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
CLOSING_CHARS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def incomplete_score(line):
    close_stack = []
    for c in line:
        if pending_close := PAREN_MAP.get(c):
            close_stack.append(pending_close)
        elif close_stack and close_stack[-1] == c:
            close_stack.pop()
        else:
            return None

    result = 0
    for c in reversed(close_stack):
        result = result * 5 + CLOSING_CHARS[c]
    return result


def main():
    scores = sorted(filter(None, (incomplete_score(line.strip()) for line in open("/Users/zee/Downloads/input-2.txt"))))
    print(scores[len(scores) // 2])


if __name__ == "__main__":
    main()
