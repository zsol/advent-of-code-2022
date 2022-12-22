import sys
from dataclasses import dataclass
from functools import cache


@dataclass(frozen=True)
class Board:
    rows: tuple[tuple[str]]

    @cache
    def row_edges(self, row_no: int) -> tuple[int, int]:
        row = self.rows[row_no]
        min_idx = 0
        max_idx = len(row) - 1
        for c in row:
            if c != " ":
                break
            min_idx += 1
        for c in reversed(row):
            if c != " ":
                break
            max_idx -= 1
        return (min_idx, max_idx)

    @cache
    def col_edges(self, col_no: int) -> tuple[int, int]:
        min_idx, max_idx = 0, len(self.rows) - 1
        for idx in range(len(self.rows)):
            if self.rows[idx][col_no] != " ":
                min_idx = idx
                break
        for _ in range(len(self.rows)):
            if self.rows[max_idx][col_no] != " ":
                break
            max_idx -= 1
        return (min_idx, max_idx)


def main() -> None:
    rows: list[tuple[str, ...]] = []
    second = sys.argv[1] == "2"
    max_col = None
    while line := sys.stdin.readline().rstrip("\n"):
        if max_col is None:
            max_col = len(line)
        if len(line) > max_col:
            raise ValueError(f"found a longer line than max_col")
        if len(line) < max_col:
            line += " " * (max_col - len(line))
        rows.append(tuple(line))

    board = Board(tuple(rows))
    directions = (
        sys.stdin.readline().rstrip().replace("R", " R ").replace("L", " L ").split(" ")
    )

    first_col = board.row_edges(0)[0]
    pos = [0, first_col]  # TODO: this might not be open
    facing = 0
    for dir in directions:
        match dir:
            case "R":
                facing = (facing + 1) % 4
            case "L":
                facing = (facing - 1) % 4
            case move:
                by = int(move)
                match facing:
                    case 0:  # right
                        vector = (0, 1)
                    case 1:  # down
                        vector = (1, 0)
                    case 2:  # left
                        vector = (0, -1)
                    case 3:  # up
                        vector = (-1, 0)
                    case _:
                        raise ValueError(f"Invalid facing {facing}")
                component = 1 - vector.index(0)
                bounds = (
                    board.row_edges(pos[0])
                    if component == 1
                    else board.col_edges(pos[1])
                )

                for _ in range(by):
                    new_pos = [pos[0] + vector[0], pos[1] + vector[1]]
                    # wrap check
                    if not second:
                        if new_pos[component] > bounds[1]:
                            new_pos[component] = bounds[0]
                        elif new_pos[component] < bounds[0]:
                            new_pos[component] = bounds[1]
                    else:
                        wrapped_pos = None
                        # this is broken somehow
                        if 0 <= new_pos[0] < 50 and new_pos[1] == 49:
                            # 1 <, 5 <; 0, 49 -> 149, 0 and 49, 49 -> 100, 0
                            wrapped_pos = [149 - new_pos[0], 0]
                        elif 50 <= new_pos[0] < 100 and new_pos[1] == 49:
                            # 3 <, 5 ^; 50, 49 -> 100, 0 and 99, 49 -> 100, 49
                            wrapped_pos = [100, new_pos[0] - 50]
                        elif 100 <= new_pos[0] < 150 and new_pos[1] == -1:
                            # 5 <, 1 <; 149, -1 -> 0, 50 and 100, -1 -> 49, 50
                            wrapped_pos = [149 - new_pos[0], 50]
                        elif 150 <= new_pos[0] < 200 and new_pos[1] == -1:
                            # 6 <, 1 ^; 150, -1 -> 0, 50 and 199, -1 -> 0, 99
                            wrapped_pos = [0, new_pos[0] - 100]
                        elif new_pos[0] == 200 and 0 <= new_pos[1] < 50:
                            # 6 v, 2 ^; 200, 0 -> 0, 100 and 200, 49 -> 0, 149
                            wrapped_pos = [0, new_pos[1] + 100]
                        elif new_pos[0] == 150 and 50 <= new_pos[1] < 100:
                            # 4 v 6 >; 150, 50 -> 150, 49 and 150, 99 -> 199, 49
                            wrapped_pos = [new_pos[1] + 100, 49]
                        elif new_pos[0] == 50 and 100 <= new_pos[1] < 150:
                            # 2 v 3 >; 50, 100 -> 50, 99 and 50, 149 -> 99, 99
                            wrapped_pos = [new_pos[1] - 50, 99]
                        elif 0 <= new_pos[0] < 50 and new_pos[1] == 150:
                            # 2 > 4 >; 0, 150 -> 149, 99 and 49, 150 -> 100, 99
                            wrapped_pos = [149 - new_pos[0], 99]
                        elif 50 <= new_pos[0] < 100 and new_pos[1] == 100:
                            # 3 > 2 v; 50, 100 -> 49, 100 and 99, 100 -> 49, 149
                            wrapped_pos = [49, new_pos[0] + 50]
                        elif 100 <= new_pos[0] < 150 and new_pos[1] == 100:
                            # 4 > 2 >; 100, 100 -> 49, 149 and 149, 100 -> 0, 149
                            wrapped_pos = [149 - new_pos[0], 149]
                        elif 150 <= new_pos[0] < 200 and new_pos[1] == 50:
                            # 6 > 4 v; 150, 50 -> 149, 50 and 199, 50 -> 149, 99
                            wrapped_pos = [149, new_pos[0] - 100]
                        elif new_pos[0] == 99 and 0 <= new_pos[1] < 50:
                            # 5 ^ 3 <; 99, 0 -> 50, 50 and 99, 49 -> 99, 50
                            wrapped_pos = [new_pos[1] + 50, 50]
                        elif new_pos[0] == -1 and 50 <= new_pos[1] < 100:
                            # 1 ^ 6 <; -1, 50 -> 150, 0 and -1, 99 -> 199, 0
                            wrapped_pos = [new_pos[1] + 100, 0]
                        elif new_pos[0] == -1 and 100 <= new_pos[1] < 150:
                            # 2 ^ 6 v; -1, 100 -> 199, 0 and -1, 149 -> 199, 49
                            wrapped_pos = [199, new_pos[1] - 100]
                        if wrapped_pos:
                            try:
                                board.rows[wrapped_pos[0]][wrapped_pos[1]]
                            except IndexError:
                                print(new_pos, wrapped_pos)
                                print(board.rows[wrapped_pos[1]])
                            new_pos = wrapped_pos

                    # wall check
                    match board.rows[new_pos[0]][new_pos[1]]:
                        case "#":
                            break
                        case ".":
                            pass
                        case other:
                            raise ValueError(
                                f"Invalid position {new_pos} ({bounds} {vector}) from {pos}"
                            )
                    pos = new_pos
    print(pos, facing)
    print((pos[0] + 1) * 1000 + (pos[1] + 1) * 4 + facing)


if __name__ == "__main__":
    main()
