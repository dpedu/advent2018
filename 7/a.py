#!/usr/bin/env python3


from time import sleep
from pprint import pprint
from collections import namedtuple, defaultdict


# Node = NamedTuple("Node", "id blocks")


def main():
    relations = defaultdict(lambda: set())  # mapping of step ID to what theyre blocked by
    steps = set()

    with open("input.txt") as f:
        for line in f.readlines():
            _, stepid, _, _, _, _, _, blocks, _, _ = line.split()
            relations[blocks].update([stepid])
            # relations[stepid].append(blocks)
            steps.update([blocks, stepid])

    # relations = dict(relations)

    # pprint(steps)
    # pprint(dict(relations))

    # while steps:
    #     sleep(1)
    #     print()
    #     print(relations)
    #     print(steps)
    #     for step in list(steps):
    #         if step not in relations or not relations[step]:
    #             print("do ", step)
    #             steps.remove(step)
    #             for otherstep, blockers in relations.items():
    #                 if step in blockers:
    #                     blockers.remove(step)
    #                 break
    #             break
    #             if step in relations:
    #                 relations[step].remove(step)

    remaining = sorted(list(steps))
    complete = set()

    while remaining:
        # print()
        # print(remaining)
        # print(dict(relations))
        # Find unblocked step
        for step in remaining[:]:
            if not relations[step]:
                # print(step, "is unblocked")
                print(step, end="")
                complete.update(step)
                for k, v in relations.items():
                    if step in v:
                        v.remove(step)
                remaining.remove(step)
                break


    # def donext():
    #     for step in remaining:
    #         pass
    #     pass

    # donext()



if __name__ == '__main__':
    main()
