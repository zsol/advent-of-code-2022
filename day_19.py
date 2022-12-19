from dataclasses import dataclass, replace
from functools import cache
import sys
from typing import TypedDict
import math


@dataclass(frozen=True)
class Resources:
    ore: int
    clay: int
    obsidian: int
    geode: int


@dataclass(frozen=True)
class Blueprint:
    ore: int
    clay: int  # ore
    obsidian: tuple[int, int]  # ore, clay
    geode: tuple[int, int]  # ore, obsidian

    def build(self, typ: str, resources: Resources) -> Resources | None:
        match typ:
            case "ore":
                if resources.ore < self.ore:
                    return None
                return replace(resources, ore=resources.ore - self.ore)
            case "clay":
                if resources.ore < self.clay:
                    return None
                return replace(resources, ore=resources.ore - self.clay)
            case "obsidian":
                if (
                    resources.ore < self.obsidian[0]
                    or resources.clay < self.obsidian[1]
                ):
                    return None
                return replace(
                    resources,
                    ore=resources.ore - self.obsidian[0],
                    clay=resources.clay - self.obsidian[1],
                )
            case "geode":
                if resources.ore < self.geode[0] or resources.obsidian < self.geode[1]:
                    return None
                return replace(
                    resources,
                    ore=resources.ore - self.geode[0],
                    obsidian=resources.obsidian - self.geode[1],
                )
            case _:
                raise ValueError(f"Invalid type {typ}")


def mine(
    miners: Resources, resources: Resources, bp: Blueprint, wait_time: int
) -> Resources:
    return Resources(
        ore=resources.ore + wait_time * miners.ore
        if miners.ore != (max_ore := max(bp.ore, bp.clay, bp.obsidian[0], bp.geode[0]))
        else max_ore,
        clay=resources.clay + wait_time * miners.clay
        if miners.clay != bp.obsidian[1]
        else bp.obsidian[1],
        obsidian=resources.obsidian + wait_time * miners.obsidian
        if miners.obsidian != bp.geode[1]
        else bp.geode[1],
        geode=resources.geode + wait_time * miners.geode,
    )


@cache
def max_geodes(
    miners: Resources, resources: Resources, bp: Blueprint, time_left: int
) -> int:
    # print(f"max_geodes({miners}, {resources}, {time_left})")
    if time_left <= 0:
        val = resources.geode
        return val

    wait_times = {
        "ore": max(0, math.ceil((bp.ore - resources.ore) / miners.ore)),
        "clay": max(0, math.ceil((bp.clay - resources.ore) / miners.ore)),
        "obsidian": max(
            0,
            math.ceil((bp.obsidian[0] - resources.ore) / miners.ore),
            math.ceil((bp.obsidian[1] - resources.clay) / miners.clay),
        )
        if miners.clay
        else -2,
        "geode": max(
            0,
            math.ceil((bp.geode[0] - resources.ore) / miners.ore),
            math.ceil((bp.geode[1] - resources.obsidian) / miners.obsidian),
        )
        if miners.obsidian
        else -2,
    }

    candidates: list[str] = []
    if miners.obsidian < bp.geode[1]:
        candidates.append("obsidian")
    if miners.clay < bp.obsidian[1]:
        candidates.append("clay")
    if miners.ore < max(bp.clay, bp.ore, bp.obsidian[0], bp.geode[0]):
        candidates.append("ore")

    known_optimal = False
    if bp.build("geode", resources):
        candidates = ["geode"]
        known_optimal = True

    build_now = [
        max_geodes(
            miners=replace(miners, **{typ: getattr(miners, typ) + 1}),
            resources=mine(miners, new_r, bp, 1),
            bp=bp,
            time_left=time_left - 1,
        )
        for typ in candidates
        if (new_r := bp.build(typ, resources))
    ]
    build_later = [
        max_geodes(
            miners=miners,
            resources=mine(miners, resources, bp, min(time_left, wait_time)),
            bp=bp,
            time_left=time_left - min(time_left, wait_time),
        )
        for wait_time in wait_times.values()
        if wait_time > 0
        if not known_optimal
    ]

    return max([0, *build_now, *build_later])


def main() -> None:
    blueprints: dict[int, Blueprint] = {}
    while line := sys.stdin.readline().rstrip():
        bp, robots = line.split(": ", 1)
        bp_id = int(bp.split(" ")[1])
        robots = robots.split(" ")
        ore = int(robots[4])
        clay = int(robots[10])
        obsidian = (int(robots[16]), int(robots[19]))
        geode = (int(robots[25]), int(robots[28]))
        blueprints[bp_id] = Blueprint(ore, clay, obsidian, geode)

    miners = Resources(ore=1, clay=0, obsidian=0, geode=0)
    resources = Resources(ore=0, clay=0, obsidian=0, geode=0)

    total_score = 0
    for i, bp in blueprints.items():
        score = max_geodes(miners, resources, bp, 24)
        total_score += score * i

    print("First", total_score)

    total_score = 1
    for bp in list(blueprints.values())[:3]:
        total_score *= max_geodes(miners, resources, bp, 32)
    print("Second", total_score)


if __name__ == "__main__":
    main()
