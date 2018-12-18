#!/usr/bin/env python3


from a import load_samples, ops, Registers


def find_opcodes(samples):
    # process of elimination to find opcode IDs

    options = {i: set(ops) for i in range(0, 16)}
    found_codes = set()
    while len(found_codes) < 15:
        for sample in samples:
            op_id = sample.instr[0]
            if op_id in found_codes:
                continue
            for op in list(options[op_id]):
                cpu = Registers(sample.before)
                op(cpu, *sample.instr[1:])
                if cpu.regs != sample.after:
                    options[op_id].remove(op)

            if len(options[op_id]) == 1:
                found_op = list(options[op_id])[0]
                found_codes.update([op_id])
                for o_opid, opset in options.items():
                    if o_opid != op_id:
                        try:
                            opset.remove(found_op)
                        except KeyError:
                            pass

    return {k: list(v)[0] for k, v in options.items()}


def main():
    samples, program = load_samples("input.txt")

    optable = find_opcodes(samples)

    cpu = Registers()

    for instruction in program:
        optable[instruction[0]](cpu, *instruction[1:])

    print("Registers:", cpu.regs)
    print("Answer:", cpu.regs[0])


if __name__ == '__main__':
    main()
