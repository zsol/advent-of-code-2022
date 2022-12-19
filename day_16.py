from dataclasses import dataclass, field, replace
from functools import cache
import sys
import re

RE = re.compile(
    r"^Valve (?P<name>[A-Z]+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<connections>.*)$"
)


@dataclass(frozen=True)
class Valve:
    name: str
    flow: int
    connections: tuple[str, ...] = field(default_factory=lambda: ())


def calculate_distances(valves: dict[str, Valve]) -> dict[tuple[str, str], int]:
    dist: dict[tuple[str, str], int] = {}
    for k, valve in valves.items():
        for conn in valve.connections:
            dist[(k, conn)] = 1
    for k in valves.keys():
        for i in valves.keys():
            for j in valves.keys():
                if (i, k) not in dist or (k, j) not in dist:
                    continue
                dist[(i, j)] = min(
                    dist.get((i, j), float("+inf")), dist[(i, k)] + dist[(k, j)]  # type: ignore
                )
    return dist


# HACK: make this global so I don't have to come up with a frozen dict type for
# functools.cache
distances: dict[tuple[str, str], int]


@cache
def potential(
    current: str,
    valves_left: frozenset[Valve],
    time_left: int,
    elephant: bool,
) -> int:
    global distances
    return max(
        [
            (
                time_after * v.flow
                + potential(v.name, valves_left - {v}, time_after, elephant)
            )
            for v in valves_left
            if (time_after := time_left - distances[(current, v.name)] - 1) >= 0
        ]
        + [
            # the remaining ones done by elephant
            potential("AA", valves_left, 26, False)
            if elephant
            else 0
        ]
    )


def main() -> None:
    valves: dict[str, Valve] = {}
    while match := RE.match(sys.stdin.readline().rstrip()):
        connections = tuple(conn_name for conn_name in match["connections"].split(", "))
        valves[match["name"]] = Valve(match["name"], int(match["flow"]), connections)

    global distances
    distances = calculate_distances(valves)
    valves_left = frozenset((valve for valve in valves.values() if valve.flow))

    print("first", potential("AA", valves_left, 30, elephant=False))

    print("second", potential("AA", valves_left, 26, elephant=True))


if __name__ == "__main__":
    main()
