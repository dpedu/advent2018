#!/usr/bin/env python3


class Node(object):
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def main():
    numplayers = 426
    lastmarb = 72058
    players = [0 for i in range(numplayers)]

    currentplr = 0
    curmarb = Node(0)
    curmarb.next = curmarb
    curmarb.prev = curmarb
    nextmarb = 1
    while True:
        if nextmarb % 23 == 0:
            remove = curmarb.prev.prev.prev.prev.prev.prev.prev
            players[currentplr] += nextmarb + remove.val
            between_a = remove.prev
            between_b = remove.next
            between_a.next = between_b
            between_b.prev = between_a
            curmarb = between_b
        else:
            place_between_a = curmarb.next
            place_between_b = place_between_a.next
            curmarb = Node(nextmarb)
            curmarb.next = place_between_b
            place_between_b.prev = curmarb
            curmarb.prev = place_between_a
            place_between_a.next = curmarb

        if nextmarb == lastmarb:
            break
        nextmarb += 1
        currentplr = (currentplr + 1) % numplayers

    print("Winning score:", max(players))


if __name__ == '__main__':
    main()
