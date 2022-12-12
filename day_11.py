from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import Callable, TextIO
import re
import math


HEADER = re.compile(r"^Monkey (\d+):$")
ITEMS = re.compile(r"^\s+Starting items: ([0-9 ,]+)$")
OP = re.compile(r"\s+Operation: new = old (?P<op>.) (?P<arg>.*)$")
TEST = re.compile(r"\s+Test: divisible by (\d+)$")
TRUE_BRANCH = re.compile(r"\s+If true: throw to monkey (\d+)$")
FALSE_BRANCH = re.compile(r"\s+If false: throw to monkey (\d+)$")


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    divisible_by: int
    true_target: int
    false_target: int

    @classmethod
    def parse(cls, input: TextIO) -> Monkey:
        if header := HEADER.match(line := input.readline().rstrip()):
            id = int(header.group(1))
        else:
            raise ValueError(f"No header match for '{line}'")
        if items_match := ITEMS.match(line := input.readline().rstrip()):
            items = [int(i) for i in items_match.group(1).split(", ")]
        else:
            raise ValueError(f"No items match for '{line}'")
        if op_match := OP.match(line := input.readline().rstrip()):
            match op_match.group("op"):
                case "+":
                    operator = int.__add__
                case "*":
                    operator = int.__mul__
                case other:
                    raise ValueError(f"Invalid operator '{other}'")
            match op_match.group("arg"):
                case "old":
                    operation: Callable[[int], int] = lambda old: operator(old, old)
                case arg:
                    operation = lambda old: operator(old, int(arg))
        else:
            raise ValueError(f"No operation match for '{line}'")
        if test_match := TEST.match(line := input.readline().rstrip()):
            divisible_by = int(test_match.group(1))
        else:
            raise ValueError(f"No test match for '{line}'")
        if true_match := TRUE_BRANCH.match(line := input.readline().rstrip()):
            true_target = int(true_match.group(1))
        else:
            raise ValueError(f"No true match for '{line}'")
        if false_match := FALSE_BRANCH.match(line := input.readline().rstrip()):
            false_target = int(false_match.group(1))
        else:
            raise ValueError(f"No false match for '{line}'")

        input.readline()  # empty line

        return Monkey(id, items, operation, divisible_by, true_target, false_target)

    def test(self, worry: int) -> bool:
        return worry % self.divisible_by == 0


def main() -> None:
    monkeys: list[Monkey] = []
    second = sys.argv[1] == "2"
    while True:
        try:
            monkeys.append(Monkey.parse(sys.stdin))
        except ValueError as e:
            print(e)
            break

    inspections = {monkey.id: 0 for monkey in monkeys}
    worry_reduction = (
        math.lcm(*[monkey.divisible_by for monkey in monkeys]) if second else None
    )

    for _ in range(10000 if second else 20):
        for monkey in monkeys:
            for item in monkey.items:
                inspections[monkey.id] += 1
                worry = monkey.operation(item)
                if worry_reduction:
                    worry %= worry_reduction
                else:
                    worry //= 3
                target = (
                    monkey.true_target if monkey.test(worry) else monkey.false_target
                )
                monkeys[target].items.append(worry)
            monkey.items = []

    top1, top2, *_ = sorted(inspections.values(), reverse=True)
    print(top1 * top2)


if __name__ == "__main__":
    main()
