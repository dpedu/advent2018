#!/usr/bin/env python3


from a import is_react


def react_poly2(poly, ignore=[]):
    lasti = 0
    while True:
        reacted = False
        for i in range(lasti, len(poly) - 1):
            if poly[i] in ignore:
                reacted = True
                poly = poly[0:i] + poly[i + 1:]
                lasti = i - 1 if i > 0 else i
                break
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

    unique_chars = set(poly.lower())
    bestlen = 99999999
    bestchar = None

    for char in unique_chars:
        chainlen = len(react_poly2(poly, [char, char.upper()]))
        if chainlen < bestlen:
            bestlen = chainlen
            bestchar = char

    print(bestlen, "by removing", bestchar)


if __name__ == '__main__':
    main()
