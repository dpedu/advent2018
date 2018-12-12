#!/usr/bin/env python3


def printstate(state):
    skeys = state.keys()
    for key in range(-30, max(skeys) + 1):
        try:
            print("#" if state[key] else ".", end="")
        except KeyError:
            print(".", end="")
    print()


def fmtrule(rule):
    return "".join(["#" if c else "." for c in rule[0]])


def main():
    state = {}
    rules = []  # list of ((True, False, True, False, True), True)
    with open("input.txt") as f:
        ogstate = f.readline()[15:-1]
        for i, c in enumerate(ogstate):
            state[i] = c == "#"
        f.readline()
        for line in f.readlines():
            tf = []
            for char in line[0:5]:
                tf.append(char == "#")
            rules.append((tuple(tf), line[-2] == "#"))

    printstate(state)

    generations = 0
    while True:
        newstate = {}
        statekeys = state.keys()
        for scankey in range(min(statekeys) - 2, max(statekeys) + 3):
            for ruleid, rule in enumerate(rules):
                matches = True
                for i, oldgenkey in zip(range(0, 5), range(scankey - 2, scankey + 3)):
                    if (oldgenkey not in state and rule[0][i]):
                        matches = False
                        break
                    elif (oldgenkey in state and rule[0][i] != state[oldgenkey]):
                        matches = False
                        break
                    # try:
                    #     if state[oldgenkey] != rule[0][i]:
                    #         matches = False
                    #         print("b1")
                    #         break
                    # except KeyError as e:
                    #     if rule[0][i]:
                    #         print("b2")
                    #         matches = False
                    #     break
                if matches and rule[1]:
                    newstate[scankey] = rule[1]
                    break
        printstate(newstate)
        state = newstate
        generations += 1
        if generations >= 20:
            break

    print(sum(state.keys()))


if __name__ == '__main__':
    main()
