import sys
import re

INSTRUCTION_RE = re.compile(
    r"^move (?P<amount>\d+) from (?P<source>\d+) to (?P<destination>\d+)$"
)


def main() -> None:
    stacks: list[list[str]] = []
    first = sys.argv[1] == "1"
    while line := sys.stdin.readline().rstrip("\n"):
        if not stacks:
            stacks = [[] for _ in range((len(line) + 1) // 4)]
        if line.startswith(" 1"):
            # stack labels; next line is separator, skip it
            sys.stdin.readline()
            stacks = [list(reversed(stack)) for stack in stacks]
            continue
        if match := INSTRUCTION_RE.match(line):
            # instructions
            amount = int(match.group("amount"))
            source = int(match.group("source")) - 1
            destination = int(match.group("destination")) - 1
            if first:
                for _ in range(amount):
                    stacks[destination].append(stacks[source].pop())
            else:
                stacks[destination].extend(stacks[source][-amount:])
                for _ in range(amount):
                    stacks[source].pop()
        else:
            # stack description
            for col in range((len(line) + 1) // 4):
                if crate := line[col * 4 + 1].strip():
                    stacks[col].append(crate)

    for stack in stacks:
        print(stack[-1], end="")


if __name__ == "__main__":
    main()
