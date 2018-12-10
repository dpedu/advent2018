#!/usr/bin/env python3


def gameround(players, currentplr, field, curmarb, nextmarb):
    """
    Simulate a round of the game.
    Clockwise is index++
    counterckw is index--

    :param players: list of players
    :param currentplr: index of the player who's turn we will simulate
    :param field: list of marbles in play
    :param curmarb: index of the current marble
    :param nextmarb: value of the marble we're about to play
    """
    if nextmarb % 23 == 0:
        # print("multiple of 23")
        players[currentplr] += nextmarb

        keep_ptr = curmarb
        keep_ptr -= 7
        keep_ptr = keep_ptr % len(field)

        players[currentplr] += field.pop(keep_ptr)
        return keep_ptr

    else:
        after_ptr = curmarb
        # advance 1 marble clockwise
        after_ptr += 1
        # looping back to the beginning
        after_ptr = after_ptr % len(field)

        # print("placing at", after_ptr + 1)
        field.insert(after_ptr + 1, nextmarb)

        return after_ptr + 1


def main():
    numplayers = 426
    lastmarb = 72058
    players = [0 for i in range(numplayers)]

    currentplr = 0
    field = [0]
    curmarb = 0
    nextmarb = 1
    while True:
        # print()
        # print("move", nextmarb)
        curmarb = gameround(players, currentplr, field, curmarb, nextmarb)
        # print("field:", field)
        # print("players:", players)
        # print("curmarb:", curmarb)
        if nextmarb == lastmarb:
            break
        nextmarb += 1
        currentplr = (currentplr + 1) % numplayers

    print("Winning score:", max(players))


if __name__ == '__main__':
    main()
