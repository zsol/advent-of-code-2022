from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def __add__(self, vector: tuple[int, int, int]) -> "Cube":
        return Cube(self.x + vector[0], self.y + vector[1], self.z + vector[2])

    def __le__(self, vector: tuple[int, int, int]) -> bool:
        return self.x <= vector[0] and self.y <= vector[1] and self.z <= vector[2]


def main() -> None:
    cubes: set[Cube] = set()
    while line := sys.stdin.readline().rstrip():
        cubes.add(Cube(*[int(num) for num in line.split(",")]))

    if sys.argv[1] == "1":
        first(cubes)
    else:
        second(cubes)


def first(cubes: set[Cube]) -> None:
    count = 0
    for cube in cubes:
        for x, y, z in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            for mult in [1, -1]:
                x *= mult
                y *= mult
                z *= mult
                neighbor = cube + (x, y, z)
                if neighbor not in cubes:
                    print(neighbor)
                    count += 1
    print(count)


all_directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]


def second(cubes: set[Cube]) -> None:
    count = 0
    xs = [cube.x for cube in cubes]
    max_x = max(xs)
    min_x = min(xs)
    ys = [cube.y for cube in cubes]
    max_y = max(ys)
    min_y = min(ys)
    zs = [cube.z for cube in cubes]
    max_z = max(zs)
    min_z = min(zs)

    for cube in cubes:
        for vec in all_directions:
            if is_external(cube + vec, cubes, min_x, max_x, min_y, max_y, min_z, max_z):
                count += 1

    print(count)


def is_external(
    candidate: Cube,
    cubes: set[Cube],
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    min_z: int,
    max_z: int,
) -> bool:
    orig_candidate = candidate
    for vec2 in all_directions:
        candidate = orig_candidate
        while candidate not in cubes:
            if not (
                min_x <= candidate.x <= max_x
                and min_y <= candidate.y <= max_y
                and min_z <= candidate.z <= max_z
            ):
                return True
            candidate = candidate + vec2
    return False


if __name__ == "__main__":
    main()
