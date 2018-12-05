#!/usr/bin/env python3


def is_react(A, B):
    """
    Return true if A and B's case differs but letter matches
    """
    return A.lower() == B.lower() and B != A


def react_poly(poly):
    lasti = 0
    while True:
        reacted = False
        for i in range(lasti, len(poly) - 1):
            if is_react(poly[i], poly[i + 1]):
                poly = poly[0:i] + poly[i + 2:]
                reacted = True
                lasti = i - 1 if i > 0 else i
                break
        if not reacted:
            break
    return poly


def main():
    with open("input.txt") as f:
        poly = f.read().strip()

    poly = react_poly(poly)

    print(len(poly))


if __name__ == '__main__':
    main()
