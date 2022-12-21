from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class Op:
    op: str
    a: str
    b: str

    def apply(self, monkeys: dict[str, int | Op]) -> int:
        match self.op:
            case "+":
                fun = int.__add__
            case "-":
                fun = int.__sub__
            case "*":
                fun = int.__mul__
            case "/":
                fun = int.__floordiv__
            case _:
                raise ValueError(f"Invalid op {self.op}")
        return fun(get(self.a, monkeys), get(self.b, monkeys))


def get(item: str, monkeys: dict[str, int | Op], no_humn: bool = False) -> int:
    entry = monkeys[item]
    if not isinstance(entry, int):
        if no_humn and "humn" in {entry.a, entry.b}:
            raise ValueError("human found")
        monkeys[item] = entry.apply(monkeys)
    return monkeys[item]  # type:ignore


def path(src: str, to: str, monkeys: dict[str, int | Op]) -> list[str]:
    if src == to:
        return [src]
    item = monkeys[src]
    if isinstance(item, int):
        return []
    for side in [item.a, item.b]:
        if ret := path(side, to, monkeys):
            ret.append(side)
            return ret
    return []


def main() -> None:
    monkeys: dict[str, int | Op] = {}
    while line := sys.stdin.readline().rstrip():
        monkey, value = line.split(":", 1)
        try:
            entry = int(value)
        except Exception:
            words = value.strip().split(" ")
            entry = Op(words[1], words[0], words[2])
        monkeys[monkey] = entry

    print("first", get("root", deepcopy(monkeys)))

    root = monkeys["root"]
    assert isinstance(root, Op)
    path_to_humn = list(reversed(path("root", "humn", monkeys)[1:]))
    other_side = root.a if path_to_humn[0] == root.b else root.b
    value = get(other_side, monkeys)
    for idx, cur in enumerate(path_to_humn[:-1]):
        item = monkeys[cur]
        assert isinstance(item, Op), cur
        other_side = item.a if path_to_humn[idx + 1] == item.b else item.b
        other_value = get(other_side, monkeys, True)
        match item.op:
            case "+":
                value -= other_value
            case "-":
                if other_side == item.a:
                    value = other_value - value
                else:
                    value += other_value
            case "*":
                value //= other_value
            case "/":
                if other_side == item.a:
                    value = other_value // value
                else:
                    value *= other_value
            case _:
                assert False, "impossible"
    print("second", value)


if __name__ == "__main__":
    main()
