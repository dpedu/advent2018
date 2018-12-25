#!/usr/bin/env python3


"""
#ip 1
 0      seti 123 0 4            set reg 4 to 123                        a = 123
 1      bani 4 456 4            set reg 4 to (register 4) & 456         a = a & 456
 2      eqri 4 72 4             set reg 4 to 1 if reg 4 == 72           a = 1 if a == 72 else 0
 3      addr 4 1 1              set reg 1 (the IP) to (IP) plus reg 4   IP = IP + a  (JUMP to 5 if the above check passes)
 4      seti 0 0 1              set IP to 0                             restart program if the above check failed

 5      seti 0 8 4              set reg 4 = 0                           a = 0               <--- reentry point from 27
 6      bori 4 65536 3          set reg 3 to reg 4 & (value)            b = a | 65536      <--- reentry point from 30
 7      seti 16098955 8 4       set reg 4 to (value)                    a = 16098955
 8      bani 3 255 5            set reg 5 to to reg 3 & (value)         c = b & 255
 9      addr 4 5 4              set reg 4 to (reg 4 plus reg 5)         a = a + c
10      bani 4 16777215 4       set reg 4 to (reg 4 & [value])          a = a & 16777215
11      muli 4 65899 4          set reg 4 to (reg 4 * [value])          a = a * 65899
12      bani 4 16777215 4       set reg 4 to (reg 4 & [value])          a = a & 16777215

13      gtir 256 3 5            set reg 5 to 1 if if [value] > reg 3    c = 1 if 256 > b
14      addr 5 1 1              set IP to IP plus reg 5                 IP = IP + c (Jump to 16 of the above check passes)
15      addi 1 1 1              set IP to IP plus 1                     Jump to 17 (else condition for above check failure)

16      seti 27 3 1             set IP to 27                            Jump to 28 if the check in 13 passed

17      seti 0 7 5              set reg 5 = 0                           c = 0

18      addi 5 1 2              set reg 2 = reg 5 + (value)             d = c + 1
19      muli 2 256 2            set reg 2 = reg 2 * (value)             d = d * 256
20      gtrr 2 3 2              set reg 2 = 1 if reg 2 > reg 3          d = 1 if d > b
21      addr 2 1 1              set IP to IP plus reg 2                 jump to 23 if above check passed (jumps to 26)
22      addi 1 1 1              set IP = to IP + 1                      jump to 24
23      seti 25 1 1                                                     jump to 26
24      addi 5 1 5              set reg 5 to reg 5 + 1                  c = c + 1
25      seti 17 6 1                                                     jump to 18
26      setr 5 4 3              set reg 3 = reg 5                       b = c
27      seti 7 5 1                                                      jump to 8

28      eqrr 4 0 5              set reg 5 to 1 if reg 4 == reg 0        if a == (MAGIC NUMBER)
29      addr 5 1 1              set IP = IP + reg 5                     End program if above check passed
30      seti 5 3 1              Jump to 6 if the check in 28 failed
"""


def main():
    while True:
        a = 123 & 456
        if a == 72:
            break

    a = 0
    aseen = set()
    while True:
        b = a | 65536
        a = 16098955
        while True:
            c = b & 255
            a += c
            a &= 16777215
            a *= 65899
            a &= 16777215
            if 256 > b:
                if a not in aseen:
                    aseen.update([a])
                    print(a)  # every time we see a new solution, we've executed the 'most' instructions.
                break
            b = b // 256


if __name__ == '__main__':
    main()
