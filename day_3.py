import sys


def main() -> None:
    total = 0
    while line := sys.stdin.readline().strip():
        first: set[str] = set(line[: len(line) // 2])
        for c in line[len(line) // 2 :]:
            if c in first:
                total += score(c)
                break
    print(total)


def main_two() -> None:
    total = 0
    lines = sys.stdin.readlines()
    while lines:
        first = set(lines.pop().strip())
        second = set(lines.pop().strip())
        third = set(lines.pop().strip())
        common = first.intersection(second).intersection(third)
        if len(common) != 1:
            raise ValueError(
                f"More than 1 common item found: {common} between ({first}, {second}, {third})"
            )
        for i in common:
            total += score(i)
    print(total)


def score(c: str) -> int:
    if "a" <= c <= "z":
        return ord(c) - ord("a") + 1
    elif "A" <= c <= "Z":
        return ord(c) - ord("A") + 27
    else:
        raise ValueError(f"Found invalid item {c}")


if __name__ == "__main__":
    if sys.argv[1] == "1":
        main()
    else:
        main_two()
