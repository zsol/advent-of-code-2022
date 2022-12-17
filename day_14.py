import sys

Stone = object()
Sand = object()

Map = list[list[None | type(Stone) | type(Sand)]]


def print_map(map: Map) -> None:
    for row in map:
        for col in row:
            if col is None:
                print(".", end="")
            elif col is Stone:
                print("#", end="")
            elif col is Sand:
                print("o", end="")
        print()


def abs_range(start: int, end: int) -> range:
    if start > end:
        return range(end, start + 1)
    else:
        return range(start, end + 1)


def main() -> None:
    infinite_floor = sys.argv[1] == "2"
    coords: list[list[tuple[int, int]]] = []
    while line := sys.stdin.readline().strip():
        pairs = line.split(" -> ")
        coords.append([tuple((int(x) for x in pair.split(","))) for pair in pairs])
    min_x = min([x for line in coords for x, _ in line])
    coords = [[(x - min_x, y) for x, y in line] for line in coords]
    max_x = max([x for line in coords for x, _ in line])
    max_y = max([y for line in coords for _, y in line])
    if infinite_floor:
        max_y += 1
    map: Map = [[None for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for pairs in coords:
        for i in range(len(pairs) - 1):
            start = pairs[i]
            end = pairs[i + 1]
            for x in abs_range(start[0], end[0]):
                for y in abs_range(start[1], end[1]):
                    map[y][x] = Stone

    sand_counter = 0
    while True:
        sand_pos_x = 500 - min_x
        sand_pos_y = 0
        in_motion = True
        # print_map(map)
        # print('=' * (max_x + 1), sand_counter)
        while in_motion and sand_pos_y < len(map) - 1:
            sand_pos_y += 1
            for candidate in [0, -1, 1]:
                if sand_pos_x + candidate > max_x or sand_pos_x + candidate < 0:
                    if not infinite_floor:
                        sand_pos_x += candidate
                        break

                    #extend the map horizontally
                    max_x += 1
                    if candidate > 0:
                        # extend the map to the right
                        for row in map:
                            row.append(None)
                    else:
                        # extend the map to the left. all coordinates shift to the right
                        for row in map:
                            row.insert(0, None)
                        sand_pos_x += 1
                        min_x -= 1
                    sand_pos_x += candidate
                    break

                if map[sand_pos_y][sand_pos_x + candidate] is None:
                    sand_pos_x += candidate
                    break
            else:
                sand_pos_y -= 1
                in_motion = not (0 <= sand_pos_x <= max_x)
        if in_motion and not infinite_floor:
            break
        map[sand_pos_y][sand_pos_x] = Sand
        sand_counter += 1
        if sand_pos_y == 0 and sand_pos_x == 500 - min_x:
            break

    print_map(map)
    print(sand_counter)


if __name__ == "__main__":
    main()
