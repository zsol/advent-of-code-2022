import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Tree:
    height: int
    visible: bool = False


def set_visibility(trees: Iterable[Tree]) -> None:
    max = None
    for tree in trees:
        if max is None or tree.height > max:
            tree.visible = True
            max = tree.height


def score(grid: list[list[Tree]], row: int, col: int) -> int:
    if row in {0, len(grid[0]) - 1} or col in {0, len(grid) - 1}:
        return 0
    tree = grid[row][col]
    left, right, top, bottom = 0, 0, 0, 0
    for i in reversed(range(0, col)):
        left += 1
        if grid[row][i].height >= tree.height:
            break

    for i in range(col + 1, len(grid[row])):
        right += 1
        if grid[row][i].height >= tree.height:
            break

    for i in reversed(range(0, row)):
        top += 1
        if grid[i][col].height >= tree.height:
            break

    for i in range(row + 1, len(grid)):
        bottom += 1
        if grid[i][col].height >= tree.height:
            break

    return left * right * top * bottom


def main() -> None:
    grid: list[list[Tree]] = []
    while line := sys.stdin.readline().strip():
        grid.append([Tree(height=int(c)) for c in line])

    for row in grid:
        set_visibility(row)  # L->R
        set_visibility(reversed(row))  # R->L

    for i in range(len(grid)):
        set_visibility((row[i] for row in grid))  # T->B
        set_visibility(row[i] for row in reversed(grid))  # B->T

    if sys.argv[1] == "1":
        print(sum([1 for row in grid for tree in row if tree.visible]))
    else:
        print(
            max(
                [
                    score(grid, i, j)
                    for i in range(len(grid))
                    for j in range(len(grid[0]))
                ]
            )
        )


if __name__ == "__main__":
    main()
