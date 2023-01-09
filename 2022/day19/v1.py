"""Day 19: Not Enough Minerals"""

import argparse
import pathlib
import re
from copy import copy


class BluePrint:
    def __init__(self, id_number, costs):
        self.id_number = id_number
        self.costs = costs
        self.max_bots = {
            bot: max(required.get(bot, 0) for required in self.costs.values())
            for bot in self.costs
        }

    def max_geodes(self, timeout):
        max_geos = 0
        states = [
            (1, dict(ore=0, cly=0, obs=0, geo=0), dict(ore=1, cly=0, obs=0, geo=0))
        ]
        while states:
            time, amts, bots = state = states.pop()

            if time == timeout:
                if amts["geo"] + bots["geo"] > max_geos:
                    max_geos = amts["geo"] + bots["geo"]
                continue

            # skip this state if max possible geos (optimistic upper bound assuming
            # a new geo bot is built every minute) is less than the actual max so far
            time_left = timeout - time
            if (
                amts["geo"]
                + bots["geo"] * (time_left + 1)
                + time_left * (time_left + 1) // 2
                < max_geos
            ):
                continue

            # no point building a non-geo bot in the last two minutes or if
            # there are already enough of them to allow building other bots
            next_bots = (
                bot
                for bot in bots
                if bot == "geo" or time < timeout - 2 and bots[bot] < self.max_bots[bot]
            )

            for bot in next_bots:
                next_state = self.build(bot, state, timeout)
                states.append(next_state)

        return max_geos

    def build(self, next_bot, state, timeout):
        required = self.costs[next_bot]
        time, amts, bots = state

        next_time = time
        next_amts = copy(amts)
        next_bots = copy(bots)

        for next_time in range(time, timeout):
            can_build = all(next_amts[res] >= required[res] for res in required)
            for res in next_amts:
                next_amts[res] += bots[res]
            if can_build:
                next_bots[next_bot] += 1
                for res in required:
                    next_amts[res] -= required[res]
                break

        return next_time + 1, next_amts, next_bots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    blueprints = []
    for line in lines:
        numbers = [int(n) for n in re.findall(r"\d+", line)]
        blueprints.append(
            BluePrint(
                id_number=numbers[0],
                costs={
                    "ore": {"ore": numbers[1]},
                    "cly": {"ore": numbers[2]},
                    "obs": {"ore": numbers[3], "cly": numbers[4]},
                    "geo": {"ore": numbers[5], "obs": numbers[6]},
                },
            )
        )

    quality = 0
    for bp in blueprints:
        max_geodes = bp.max_geodes(timeout=24)
        print("(1) blueprint:", bp.id_number, max_geodes)
        quality += bp.id_number * max_geodes
    print("part 1:", quality)

    product = 1
    for bp in blueprints[:3]:
        max_geodes = bp.max_geodes(timeout=32)
        print("(2) blueprint:", bp.id_number, max_geodes)
        product *= max_geodes
    print("part 2:", product)


if __name__ == "__main__":
    main()
