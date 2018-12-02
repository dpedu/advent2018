#!/usr/bin/env python3


def main():
    total = 0
    with open("input.txt") as f:
        for line in f.readlines():
            total += int(line)
    print(total)


if __name__ == '__main__':
    main()
