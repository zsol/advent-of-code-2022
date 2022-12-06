import sys
from heapq import heappushpop, heappush


def main() -> None:
    two(int(sys.argv[1]))


def one() -> None:
    cal_list = sys.stdin.readlines()
    max_value = 0
    current = 0
    for line in cal_list:
        if item := line.strip():
            current += int(item)
        else:
            if current > max_value:
                max_value = current
            current = 0

    print(max_value)


def two(elf_count: int = 3) -> None:
    cal_list = sys.stdin.readlines()
    top = []
    current = 0
    for line in cal_list:
        if item := line.strip():
            current += int(item)
            continue
        if len(top) < elf_count:
            heappush(top, current)
        elif current > top[0]:
            heappushpop(top, current)
        current = 0
    print(sum(top))


if __name__ == "__main__":
    main()
