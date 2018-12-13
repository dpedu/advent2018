#!/usr/bin/env python3


from a import loadboard, advancecart


def main():
    board, carts = loadboard("input.txt")

    while True:
        # Put carts in processing order
        carts.sort(key=lambda cart: cart.coord)
        # this time we separately track cars remaining to be processed in the tick, so that in the event of a collision
        # we can remove the second cart from this queue,
        toprocess = carts[:]
        while toprocess:
            cart = toprocess.pop(0)
            collision, crashee = advancecart(cart, carts, board)
            if collision:
                # Remove both carts from the game
                carts.remove(crashee)
                carts.remove(cart)
                try:
                    # Remove the cart we hit from the work queue, if possible
                    toprocess.remove(crashee)
                except ValueError:
                    pass
        if len(carts) == 1:
            print(carts[0].coord)
            break


if __name__ == '__main__':
    main()
