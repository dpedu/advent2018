#!/usr/bin/env python3


def main():
    number = 10551276  # from r5 in b_helper.py
    ssum = 0
    for i in range(1, 10551276 + 1):
        if number % i == 0:
            ssum += i

    print(ssum)

if __name__ == '__main__':
    main()
