#!/usr/bin/env python3


"""
four registers (numbered 0 through 3) that
can be manipulated by instructions containing one of 16 opcodes.
The registers start with the value 0.

Every instruction consists of four values:
    an opcode,
    two inputs (named A and B), and
    an output (named C), in that order.

The opcode specifies the behavior of the instruction and how the inputs are interpreted.
The output, C, is always treated as a register.

ch opcode has a number from 0 through 15
"""


def addr(regs, a, b, c):
    # addr (add register) stores into register C the result of adding register A and register B.
    regs.set(c, regs.get(a) + regs.get(b))


def addi(regs, a, b, c):
    # addi (add immediate) stores into register C the result of adding register A and value B.
    regs.set(c, regs.get(a) + b)


def mulr(regs, a, b, c):
    # mulr (multiply register) stores into register C the result of multiplying register A and register B.
    regs.set(c, regs.get(a) * regs.get(b))


def muli(regs, a, b, c):
    # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    regs.set(c, regs.get(a) * b)


def banr(regs, a, b, c):
    # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    regs.set(c, regs.get(a) & regs.get(b))


def bani(regs, a, b, c):
    # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    regs.set(c, regs.get(a) & b)


def borr(regs, a, b, c):
    # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    regs.set(c, regs.get(a) | regs.get(b))


def bori(regs, a, b, c):
    # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    regs.set(c, regs.get(a) | b)


def setr(regs, a, b, c):
    # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    regs.set(c, regs.get(a))


def seti(regs, a, b, c):
    # seti (set immediate) stores value A into register C. (Input B is ignored.)
    regs.set(c, a)


def gtir(regs, a, b, c):
    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    regs.set(c, 1 if a > regs.get(b) else 0)


def gtri(regs, a, b, c):
    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) > b else 0)


def gtrr(regs, a, b, c):
    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) > regs.get(b) else 0)


def eqir(regs, a, b, c):
    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    regs.set(c, 1 if a == regs.get(b) else 0)


def eqri(regs, a, b, c):
    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) == b else 0)


def eqrr(regs, a, b, c):
    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) == regs.get(b) else 0)


ops = (addr,
       addi,
       mulr,
       muli,
       banr,
       bani,
       borr,
       bori,
       setr,
       seti,
       gtir,
       gtri,
       gtrr,
       eqir,
       eqri,
       eqrr)


class Registers(object):
    def __init__(self, initial=None):
        self.regs = list(initial) if initial else [0, 0, 0, 0]

    def get(self, num):
        return self.regs[num]

    def set(self, num, value):
        self.regs[num] = value


class SampleInstr(object):
    def __init__(self, before, instr, after):
        self.before = before
        self.instr = instr
        self.after = after


def load_samples(fname):
    """
    Load the samples into a list
    """
    samples = []
    program = []
    with open(fname) as f:
        while True:
            line = f.readline()
            if not line.startswith("Before"):
                break
            samples.append(SampleInstr(
                [int(i) for i in line.strip().split(": [")[1][0:-1].split(", ")],
                [int(i) for i in f.readline().strip().split()],
                [int(i) for i in f.readline().strip().split(":  [")[1][0:-1].split(", ")]))
            f.readline()

        f.readline()
        for line in f.readlines():
            program.append([int(i) for i in line.strip().split()])

    return samples, program


def run_sample(sample, op):
    # Run the sample through one opcode and returns True if our output matches the sample output
    r = Registers(sample.before)
    op(r, *sample.instr[1:])
    return sample.after == r.regs


def sample_repeats(sample):
    # run the sample through the opcodes until a duplicate result is found
    matching = 0
    for op in ops:
        if run_sample(sample, op):
            matching += 1
        if matching >= 3:
            return True
    return False


def main():
    samples, _ = load_samples("input.txt")

    repeating = 0
    for sample in samples:
        if sample_repeats(sample):
            repeating += 1

    print(repeating)


if __name__ == '__main__':
    main()
