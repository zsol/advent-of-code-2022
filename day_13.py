from __future__ import annotations

import json

import sys
from functools import cmp_to_key
from typing import cast, Union

Packet = list[Union[int, "Packet"]]


def compare(first: Packet, second: Packet) -> bool | None:
    if len(first) == 0:
        return True
    if len(second) == 0:
        return False
    fhead = first[0]
    shead = second[0]
    if fhead == shead:
        return compare(first[1:], second[1:])
    if isinstance(fhead, int) and isinstance(shead, int):
        return fhead < shead
    elif isinstance(fhead, list) and isinstance(shead, int):
        return compare(first, [[shead], *second[1:]])
    elif isinstance(fhead, int) and isinstance(shead, list):
        return compare([[fhead], *first[1:]], second)
    else:  # both are lists
        if (result := compare(fhead, shead)) is None:
            return compare(first[1:], second[1:])
        else:
            return result


def main() -> None:
    first, second = None, None
    count = 0
    index = 0
    while line := sys.stdin.readline():
        if first is None:
            first = cast(Packet, json.loads(line))
        elif second is None:
            second = cast(Packet, json.loads(line))
            index += 1
            if compare(first, second):
                count += index
        elif not line.rstrip():
            first, second = None, None
        else:
            raise ValueError("Invalid input")
    print(count)


def second_main() -> None:
    packets = [
        cast(Packet, json.loads(line)) for line in sys.stdin.readlines() if line.strip()
    ]
    first: Packet = [[2]]
    second: Packet = [[6]]
    packets.extend([first, second])
    packets.sort(key=cmp_to_key(lambda x, y: -1 if compare(x, y) else 1))

    first_ind = packets.index(first) + 1
    second_ind = packets.index(second) + 1
    print(first_ind * second_ind)


if __name__ == "__main__":
    if sys.argv[1] == "2":
        second_main()
    else:
        main()
