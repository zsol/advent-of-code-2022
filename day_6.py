import sys


def main() -> None:
    line = sys.stdin.readline().strip()
    buf: list[str] = []
    marker_length = int(sys.argv[1])
    for idx, c in enumerate(line):
        buf.append(c)
        if len(buf) < marker_length:
            continue
        if len(buf) > marker_length:
            buf.pop(0)
        if len(set(buf)) == marker_length:
            print(idx + 1)
            return
    return


if __name__ == "__main__":
    main()
