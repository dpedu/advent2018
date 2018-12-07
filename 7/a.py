#!/usr/bin/env python3

from collections import defaultdict


def main():
    relations = defaultdict(lambda: set())  # mapping of step ID to what theyre blocked by
    steps = set()

    with open("input.txt") as f:
        for line in f.readlines():
            _, stepid, _, _, _, _, _, blocks, _, _ = line.split()
            relations[blocks].update([stepid])
            steps.update([blocks, stepid])

    remaining = sorted(list(steps))
    complete = set()

    while remaining:
        for step in remaining[:]:
            # find unblocked step
            if not relations[step]:
                print(step, end="")
                complete.update(step)
                # remove the completed step from the blockers of other steps
                for k, v in relations.items():
                    if step in v:
                        v.remove(step)
                remaining.remove(step)
                break
    print()


if __name__ == '__main__':
    main()
