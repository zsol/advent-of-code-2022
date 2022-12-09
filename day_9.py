from __future__ import annotations
import sys
from dataclasses import dataclass, replace
from math import sqrt


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def distance_from(self, pos: Position) -> int:
        return int(sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2))

    def move_towards(self, pos: Position) -> Position:
        xadj = (xdiff // abs(xdiff)) if (xdiff := pos.x - self.x) != 0 else 0
        yadj = (ydiff // abs(ydiff)) if (ydiff := pos.y - self.y) != 0 else 0
        return replace(self, x=self.x + xadj, y=self.y + yadj)


def main() -> None:
    head = Position(0, 0)
    tailcount = int(sys.argv[1])
    tails = [Position(0, 0) for _ in range(tailcount)]
    rope = [head, *tails]
    visited: set[Position] = set()
    visited.add(rope[-1])
    while line := sys.stdin.readline().strip():
        dir, amount = line[0], int(line[2:])
        for _ in range(amount):
            match dir:
                case "U":
                    rope[0] = replace(rope[0], y=rope[0].y + 1)
                case "D":
                    rope[0] = replace(rope[0], y=rope[0].y - 1)
                case "L":
                    rope[0] = replace(rope[0], x=rope[0].x - 1)
                case "R":
                    rope[0] = replace(rope[0], x=rope[0].x + 1)
                case _:
                    raise ValueError(f"Invalid instruction {dir}")
            for ind in range(len(rope) - 1):
                next = ind + 1
                if rope[next].distance_from(rope[ind]) > 1:
                    rope[next] = rope[next].move_towards(rope[ind])
            visited.add(rope[-1])
    print(len(visited))


if __name__ == "__main__":
    main()
