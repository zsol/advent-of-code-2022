import sys
from typing import Tuple


def main() -> None:
    cycle = 0
    x = 1
    total_signal = 0
    while line := sys.stdin.readline().strip():
        instr, *params = line.split(" ")
        cycle, x, signal = process(cycle, instr, int(params[0]) if params else None, x)
        total_signal += signal
    print(total_signal)


def process(
    cycle: int, instr: str, param: int | None, orig_x: int
) -> Tuple[int, int, int]:
    duration = 0
    x = orig_x
    match instr:
        case "noop":
            duration = 1
        case "addx":
            duration = 2
            assert param is not None
            x += param
        case _:
            raise ValueError(f"Invalid instruction {instr}")
    signal = 0
    for i in range(cycle + 1, cycle + duration + 1):
        position = (i - 1) % 40
        if i % 40 == 20:
            signal += i * orig_x
        if orig_x - 1 <= position <= orig_x + 1:
            print("#", end="")
        else:
            print(".", end="")
        if position == 39:
            print()
    return (cycle + duration, x, signal)


if __name__ == "__main__":
    main()
