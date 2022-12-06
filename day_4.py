import sys


def get_range(pair: str) -> tuple[int, int]:
    first, second = pair.split("-")
    return int(first), int(second)


def main() -> None:
    count = 0
    one = sys.argv[1] == "1"
    while line := sys.stdin.readline().strip():
        first, second = line.split(",")
        fs, fe = get_range(first)
        ss, se = get_range(second)
        if one:
            if (fs <= ss and se <= fe) or (ss <= fs and fe <= se):
                count += 1
        else:
            if (
                (fs <= ss <= fe)
                or (fs <= se <= fe)
                or (ss <= fs <= se)
                or (ss <= fe <= se)
            ):
                count += 1
    print(count)


if __name__ == "__main__":
    main()
