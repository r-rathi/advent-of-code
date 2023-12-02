"""Day 2: Cube Conundrum"""

import argparse
import pathlib
from math import prod


def part1(games):
    max_cubes = dict(red=12, green=13, blue=14)
    possible_games = []
    for game_id, draws in games:
        possible = True
        for draw in draws:
            for color, max_count in max_cubes.items():
                if draw.get(color, 0) > max_count:
                    possible = False
                    break
        if possible:
            possible_games.append(game_id)
    # print(possible_games)
    return sum(possible_games)


def part2(games):
    powers = []
    for game_id, draws in games:
        min_cubes = dict(red=0, green=0, blue=0)
        for draw in draws:
            for color in min_cubes:
                if draw.get(color, 0) > min_cubes[color]:
                    min_cubes[color] = draw.get(color, 0)
        power = prod(min_cubes.values())
        powers.append(power)
        # print(game_id, min_cubes, power)
    return sum(powers)


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    games = []
    for line in lines:
        game, plays = line.split(":")
        game_id = int(game.strip().split()[1])
        draws = []
        for play in plays.strip().split(";"):
            draw = [draw.strip().split() for draw in play.strip().split(",")]
            cubes = {color: int(count) for count, color in draw}
            draws.append(cubes)
        games.append((game_id, draws))
    # print(games)

    print("part 1:", part1(games))
    print("part 2:", part2(games))


if __name__ == "__main__":
    main()
