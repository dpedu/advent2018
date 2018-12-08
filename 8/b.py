#!/usr/bin/env python3


def getnodevalue(data):
    """
    Get the current node value
    - parse number of child nodes

    """

    children_count = data.pop(0)
    meta_count = data.pop(0)

    if children_count == 0:
        value = 0
        while meta_count > 0:
            meta_count -= 1
            value += data.pop(0)
        return value
    else:
        child_values = []
        while children_count > 0:
            children_count -= 1
            child_values.append(getnodevalue(data))
        value = 0
        while meta_count > 0:
            meta_count -= 1
            entry = data.pop(0)
            if entry <= len(child_values):
                value += child_values[entry - 1]
        return value


def main():
    with open("input.txt") as f:
        numbers = [int(i) for i in f.read().split()]

    mdtotal = getnodevalue(numbers)

    print(mdtotal)


if __name__ == '__main__':
    main()
