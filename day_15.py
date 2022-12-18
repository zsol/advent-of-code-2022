from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from functools import cached_property

INPUT_RE = re.compile(
    r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$"
)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def distance(self, other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Sensor:
    position: Position
    nearest_beacon: Position

    _covered_positions: set[Position] = field(init=False)

    # def __post_init__(self) -> None:
    #     self._covered_positions = set()
    #     for x in range(self.position.x - self.coverage, self.position.x + self.coverage+1):
    #         for y in range(self.position.y - self.coverage + abs(x - self.position.x), self.position.y + self.coverage - abs(x - self.position.x)):
    #             self._covered_positions.add(Position(x, y))
    #             assert not self.possible_beacon(Position(x, y))

    @cached_property
    def coverage(self) -> int:
        return self.position.distance(self.nearest_beacon)

    def possible_beacon(self, pos: Position) -> bool:
        if pos == self.nearest_beacon:
            return True
        # return pos in self._covered_positions
        return pos.distance(self.position) > self.coverage


def main() -> None:
    sensors: list[Sensor] = []
    while line := sys.stdin.readline().rstrip():
        if not (match := INPUT_RE.match(line)):
            raise ValueError(f"Invalid input: {line}")
        sensors.append(
            Sensor(
                Position(int(match[1]), int(match[2])),
                nearest_beacon=Position(int(match[3]), int(match[4])),
            )
        )
    count = 0
    if sys.argv[1] == "2":
        y = 0
        while y <= 4_000_000:
            x = 0
            while x <= 4_000_000:
                point = Position(x, y)
                if 0 < (
                    min_distance := min(
                        [
                            sensor.position.distance(point) - sensor.coverage
                            for sensor in sensors
                        ]
                    )
                ):
                    # we're outside of all circles, we found the point
                    print(x * 4_000_000 + y)
                    return
                else:
                    x += abs(min_distance) + 1
            y += 1
    else:
        y = 2000000
        min_x = min([sensor.position.x - sensor.coverage for sensor in sensors])
        max_x = max([sensor.position.x + sensor.coverage for sensor in sensors])

        # The naive implementation was too slow
        # for x in range(min_x, max_x + 1):
        #     if any((not sensor.possible_beacon(Position(x, y)) for sensor in sensors)):
        #         count += 1

        x = min_x
        while x <= max_x:
            if 0 < (
                min_distance := min(
                    [
                        sensor.position.distance(Position(x, y)) - sensor.coverage
                        for sensor in sensors
                    ]
                )
            ):
                # we're outside of all circles
                x += min_distance
            elif 0 == min_distance and any(
                (sensor.nearest_beacon == Position(x, y) for sensor in sensors)
            ):
                # this is an actual beacon
                x += 1
            else:
                # we're inside at least one circle, min_distance is the distance to the
                # edge of the biggest circle we're in
                x += abs(min_distance) + 1
                count += abs(min_distance) + 1
        print(count)


if __name__ == "__main__":
    main()
