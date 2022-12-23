from __future__ import annotations
import sys
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def adjancent(self, direction: int) -> list[Position]:
        match direction:
            case 0:  # North
                return [
                    replace(self, row=self.row - 1, col=self.col - 1),
                    replace(self, row=self.row - 1),
                    replace(self, row=self.row - 1, col=self.col + 1),
                ]
            case 1:  # South
                return [
                    replace(self, row=self.row + 1, col=self.col - 1),
                    replace(self, row=self.row + 1),
                    replace(self, row=self.row + 1, col=self.col + 1),
                ]
            case 2:  # West
                return [
                    replace(self, row=self.row - 1, col=self.col - 1),
                    replace(self, col=self.col - 1),
                    replace(self, row=self.row + 1, col=self.col - 1),
                ]
            case 3:  # East
                return [
                    replace(self, row=self.row - 1, col=self.col + 1),
                    replace(self, col=self.col + 1),
                    replace(self, row=self.row + 1, col=self.col + 1),
                ]
            case _:
                raise ValueError("Invalid facing")


next_elf_id = 0


def next_id() -> int:
    global next_elf_id
    next_elf_id += 1
    return next_elf_id - 1


@dataclass(frozen=True)
class Elf:
    id: int = field(default_factory=next_id)


def main() -> None:
    elves: dict[Position, Elf] = {}
    positions: dict[Elf, Position] = {}
    row = 0
    while line := sys.stdin.readline().rstrip():
        for idx, c in enumerate(line):
            if c == "#":
                pos = Position(row, idx)
                elf = Elf()
                elves[pos] = elf
                positions[elf] = pos
        row += 1

    round = 0
    while True:
        new_elves: dict[Position, Elf | None] = {}
        for pos, elf in elves.items():
            proposal = None
            seen_neighbor = False
            for dir in range(4):
                new_facing = (round + dir) % 4
                adjacent = pos.adjancent(new_facing)
                if all(adj not in elves for adj in adjacent):
                    if proposal is None:
                        proposal = adjacent[1]
                else:
                    seen_neighbor = True
            if not seen_neighbor or not proposal:
                # don't move
                # this is safe because elves will never propose to move near one another
                new_elves[pos] = elf
                continue

            if proposal in new_elves:
                new_elves[pos] = elf
                if conflicting_elf := new_elves[proposal]:
                    # fixup conflicting elf
                    old_pos = positions[conflicting_elf]
                    new_elves[old_pos] = conflicting_elf
                    # mark location as conflicting
                    new_elves[proposal] = None
            else:
                new_elves[proposal] = elf

        # round over, update elves and positions
        round += 1
        if elves == new_elves:
            break
        elves = {pos: elf for pos, elf in new_elves.items() if elf}
        positions = {elf: pos for pos, elf in elves.items()}
        if round == 10:
            # calculate bounding box and count empty spaces
            min_row = min([pos.row for pos in elves.keys()])
            min_col = min([pos.col for pos in elves.keys()])
            max_row = max([pos.row for pos in elves.keys()])
            max_col = max([pos.col for pos in elves.keys()])
            print(
                "first",
                sum(
                    1
                    for row in range(min_row, max_row + 1)
                    for col in range(min_col, max_col + 1)
                    if Position(row, col) not in elves
                ),
            )
    print("second", round)


if __name__ == "__main__":
    main()
