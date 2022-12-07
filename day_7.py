import sys
from pathlib import Path
from typing import Generator, Tuple


def entry(tree: dict[str, dict | int], path: Path) -> dict | int:
    cur = tree
    for subdir in path.parts:
        if subdir not in cur:
            cur[subdir] = {}
        cur = cur[subdir]
    return cur


def size(tree: dict[str, dict | int]) -> Generator[Tuple[str, int], None, int]:
    total = 0
    for name, item in tree.items():
        if isinstance(item, dict):
            item_size = yield from size(item)
            yield (name, item_size)
        else:
            item_size = item
        total += item_size

    return total


def main() -> None:
    cmd = None
    cwd = Path("/")
    tree = {}
    while line := sys.stdin.readline().strip():
        if line[0] == "$":
            cmd, *arg = line[2:].split(" ", 1)
            match cmd:
                case "cd":
                    match arg:
                        case [".."]:
                            cwd = cwd.parent
                        case ["/"]:
                            cwd = Path("/")
                        case [dir]:
                            cwd = cwd / dir
                        case _:
                            raise RuntimeError("impossible")
                case _:
                    pass
            continue
        if line.startswith("dir"):
            entry(tree, cwd / line[4:])
            continue
        sz, file = line.split(" ", 1)
        entry(tree, cwd)[file] = int(sz)

    if sys.argv[1] == "1":
        print(sum([sz for name, sz in size(tree) if sz <= 100000]))
    else:
        disk_space = 70000000
        required = 30000000
        sizes = list(size(tree))
        used = sizes[-1][1]
        unused = disk_space - used
        to_delete = required - unused
        if to_delete <= 0:
            print(0)
            return
        print(min([sz for _, sz in sizes if sz >= to_delete]))


if __name__ == "__main__":
    main()
