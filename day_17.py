from collections import defaultdict
import sys
import itertools

Chamber = list[list[str]]
Rock = list[tuple[int, int]]
CHAMBER_WIDTH = 7
EMPTY_ROW = [" "] * CHAMBER_WIDTH


def rock_at(height: int, typ: str) -> Rock:
    match typ:
        case "-":
            return [(2, height), (3, height), (4, height), (5, height)]
        case "+":
            return [
                (3, height),
                (2, height + 1),
                (3, height + 1),
                (4, height + 1),
                (3, height + 2),
            ]
        case "L":
            return [
                (2, height),
                (3, height),
                (4, height),
                (4, height + 1),
                (4, height + 2),
            ]
        case "|":
            return [(2, height), (2, height + 1), (2, height + 2), (2, height + 3)]
        case "o":
            return [(2, height), (3, height), (2, height + 1), (3, height + 1)]
        case _:
            raise ValueError(f"Invalid rock type: {typ}")


def shift(chamber: Chamber, rock: Rock, offset: int) -> Rock:
    new_rock = [(x + offset, y) for x, y in rock]
    if not collision(chamber, new_rock):
        return new_rock
    return rock


def fall(rock: Rock) -> Rock:
    return [(x, y - 1) for x, y in rock]


def chamber_top(chamber: Chamber) -> int:
    for height, row in enumerate(chamber):
        if row == EMPTY_ROW:
            return height
    return len(chamber)


def print_chamber(chamber: Chamber) -> None:
    for row in reversed(chamber):
        print("|", end="")
        for c in row:
            print(c, end="")
        print("|")
    print(f'+{"-" * CHAMBER_WIDTH}+\n')


def collision(chamber: Chamber, rock: Rock) -> bool:
    return (
        any(not (0 <= x < CHAMBER_WIDTH) for x, _ in rock)
        or any(y < 0 for _, y in rock)
        or any(chamber[y][x] != " " for x, y in rock)
    )


TARGET_ROUND = 1000000000000


def main() -> None:
    rock_types = "-+L|o"
    rock_index = 0
    jetstream = sys.stdin.readline().rstrip()
    jet_index = 0
    chamber: Chamber = []
    top = 0
    cycles: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for rock_num in range(len(rock_types) * len(jetstream)):
        if rock_num == 2022:
            print(f"First: {top}")
        cycles[(rock_index, jet_index)].append((rock_num, top))
        rock = rock_at(top + 3, rock_types[rock_index])
        rock_index = (rock_index + 1) % len(rock_types)
        max_y = max([y for _, y in rock])
        for _ in range(len(chamber) - 1, max_y + 1):
            chamber.append(list(EMPTY_ROW))
        while True:
            match jetstream[jet_index]:
                case "<":
                    rock = shift(chamber, rock, -1)
                case ">":
                    rock = shift(chamber, rock, 1)
                case jet:
                    raise ValueError(f"Jet {jet} invalid")
            jet_index = (jet_index + 1) % len(jetstream)
            fallen_rock = fall(rock)
            if collision(chamber, fallen_rock):
                break
            rock = fallen_rock
        for x, y in rock:
            chamber[y][x] = "#"
        top = max(top, *[y + 1 for _, y in rock])

    cycle_start_idx: None | tuple[int, int] = None
    cycle_lengths: dict[tuple[int, int], int] = {}
    cycle_heights: dict[tuple[int, int], int] = {}
    for idx, rocks in cycles.items():
        if len(rocks) == 1:
            cycle_heights[idx] = rocks[0][1]
            continue
        cycle_heights[idx] = rocks[-1][1] - rocks[-2][1]
        cycle_lengths[idx] = rocks[-1][0] - rocks[-2][0]
        if (TARGET_ROUND - rocks[0][0]) % cycle_lengths[idx] == 0:
            cycle_start_idx = idx

    if cycle_start_idx is None:
        raise ValueError("cycle not found")

    prelude_round, prelude_height = cycles[cycle_start_idx][0]
    cycle_length = cycle_lengths[cycle_start_idx]
    cycle_height = cycle_heights[cycle_start_idx]

    print(
        f"Second: {prelude_height + (TARGET_ROUND - prelude_round) * cycle_height // cycle_length}"
    )


if __name__ == "__main__":
    main()
