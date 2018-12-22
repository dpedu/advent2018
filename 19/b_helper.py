#!/usr/bin/env python3


from a import Cpu
import pdb


def main():
    setip = None
    program = []
    with open("input.txt") as f:
        setip = int(f.readline().strip().split()[-1])
        for line in f.readlines():
            instr, *params = line.strip().split()
            program.append([instr] + [int(p) for p in params])

    cpu = Cpu([1, 0, 0, 0, 0, 0])
    cpu.ipreg = setip

    ip = 0
    cycles = 0
    while ip < len(program):
        instr = program[ip]
        # if cycles % 1000 == 0:
        cpu.ip = ip
        ip = cpu.execute(instr[0], instr[1:])
        ip += 1
        cycles += 1

        print("IP={:<2}, INSTR={:<18}, REGS={}".format(ip, str(instr), cpu.regs))

        if cpu.regs[setip] == 10:
            pdb.set_trace()


if __name__ == '__main__':
    main()
