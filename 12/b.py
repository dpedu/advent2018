#!/usr/bin/env python3


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

            if line[-2] != "#":  # turns out these didn't matter...?
                continue
            rules.append((tuple(tf), line[-2] == "#"))

    generations = 0
    target = 50000000000
    lastvalues = []
    lastvalue = 0

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
                if matches:
                    newstate[scankey] = rule[1]
                    break
        state = newstate

        value = sum(state.keys())
        lastvalues.append(value - lastvalue)
        lastvalue = value
        if len(lastvalues) > 5:
            if len(set(lastvalues)) == 1:
                print("Convergence on delta", lastvalues[0], "at generation", generations)
                remaining = target - generations
                print(value + lastvalues[0] * (remaining - 1))
                break
            lastvalues.pop(0)

        generations += 1
        if generations >= target:
            break


if __name__ == '__main__':
    main()
