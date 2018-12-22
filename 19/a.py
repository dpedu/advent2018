#!/usr/bin/env python3


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
    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if a > regs.get(b) else 0)


def gtri(regs, a, b, c):
    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) > b else 0)


def gtrr(regs, a, b, c):
    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) > regs.get(b) else 0)


def eqir(regs, a, b, c):
    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if a == regs.get(b) else 0)


def eqri(regs, a, b, c):
    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) == b else 0)


def eqrr(regs, a, b, c):
    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B.
    # Otherwise, register C is set to 0.
    regs.set(c, 1 if regs.get(a) == regs.get(b) else 0)


opsfuncs = (addr,
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


ops = {op.__name__: op for op in opsfuncs}


class Cpu(object):
    def __init__(self, initial=None):
        self.ipreg = None
        self.regs = list(initial) if initial else [0] * 6

    def get(self, num):
        return self.regs[num]

    def set(self, num, value):
        self.regs[num] = value

    def execute(self, instr, params):
        """
        Execute an instruction and return the new instruction pointer value
        """
        self.regs[self.ipreg] = self.ip
        ops[instr](self, *params)
        return self.regs[self.ipreg]


def main():
    setip = None
    program = []
    with open("input.txt") as f:
        setip = int(f.readline().strip().split()[-1])
        for line in f.readlines():
            instr, *params = line.strip().split()
            program.append([instr] + [int(p) for p in params])

    cpu = Cpu()
    cpu.ipreg = setip

    ip = 0
    while ip < len(program):
        instr = program[ip]
        cpu.ip = ip
        ip = cpu.execute(instr[0], instr[1:])
        ip += 1

    print(cpu.regs[0])


if __name__ == '__main__':
    main()
