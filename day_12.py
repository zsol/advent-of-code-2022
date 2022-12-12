import sys
from typing import Tuple

Position = Tuple[int, int]


def legal_move(fro: Position, to: Position, map: list[list[int]]) -> bool:
    return (
        0 <= fro[0] < len(map)
        and 0 <= to[0] < len(map)
        and 0 <= fro[1] < len(map[fro[0]])
        and 0 <= to[1] < len(map[to[0]])
        and map[fro[0]][fro[1]] + 1 >= map[to[0]][to[1]]
    )


def main() -> None:
    map: list[list[int]] = []
    positions: set[Position] = set()
    end_positions: set[Position] = set()
    stepcount = 0

    while line := sys.stdin.readline().rstrip():
        if "S" in line:
            # starting position
            positions.add((len(map), line.find("S")))
        if "E" in line:
            # ending position
            end_positions.add((len(map), line.find("E")))
        map.append(
            [ord("a") if c == "S" else ord("z") if c == "E" else ord(c) for c in line]
        )
    if sys.argv[1] == "2":
        for x, row in enumerate(map):
            for y, col in enumerate(row):
                if col == ord("a"):
                    positions.add((x, y))
    while positions:
        old_positions = set(positions)
        positions = set()
        stepcount += 1
        for posx, posy in old_positions:
            for x, y in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                newpos = (posx + x), (posy + y)
                if legal_move((posx, posy), newpos, map):
                    positions.add(newpos)
                    if newpos in end_positions:
                        print(stepcount)
                        return


if __name__ == "__main__":
    main()
