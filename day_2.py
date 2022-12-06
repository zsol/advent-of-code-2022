import sys


def main() -> None:
    first = len(sys.argv) <= 1 or sys.argv[1] == "1"
    total = 0
    while line := sys.stdin.readline().strip():
        their_str, second = line.split(" ")
        their = ord(their_str) - ord("A")
        if first:
            mine = ord(second) - ord("X")
        else:
            mine = get_mine(their, second)
        total += get_score(their, mine)
    print(total)


def get_score(their: int, mine: int) -> int:
    match (mine - their) % 3:
        case 0:  # draw
            score = 3
        case 1:  # win
            score = 6
        case 2:  # loss
            score = 0
        case _:
            raise RuntimeError("impossible")
    return score + mine + 1


def get_mine(their: int, second: str) -> int:
    match second:
        case "X":  # loss
            mine = (their + 2) % 3
        case "Y":  # draw
            mine = their  # % 3 is assumed
        case "Z":
            mine = (their + 1) % 3
        case _:
            raise ValueError(f"Unexpected result {second}")
    return mine


if __name__ == "__main__":
    main()
