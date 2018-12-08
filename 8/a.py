#!/usr/bin/env python3


def main():
    with open("input2.txt") as f:
        numbers = [int(i) for i in f.read().split()]
    mdtotal = 0

    def parseit(data):
        nonlocal mdtotal
        children = data.pop(0)
        metas = data.pop(0)

        while children > 0:
            children -= 1
            parseit(data)

        while metas > 0:
            metas -= 1
            mdtotal += data.pop(0)

    parseit(numbers)
    print(mdtotal)


if __name__ == '__main__':
    main()
