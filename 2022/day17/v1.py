"""Day 17: Pyroclastic Flow"""
import pathlib
import sys
import time

# 0  XXXX
#
# 1  .X.
#    XXX
#    .X.
#
# 2  ..X
#    ..X
#    XXX
#
# 3  X
#    X
#    X
#    X
#
# 4  XX
#    XX

ROCK_WH = [
    (4, 1),
    (3, 3),
    (3, 3),
    (1, 4),
    (2, 2),
]

ROCK = [
    [0b1111],
    [0b010, 0b111, 0b010],
    [0b111, 0b001, 0b001],
    [0b1, 0b1, 0b1, 0b1],
    [0b11, 0b11],
]


def rocks():
    n = 5
    i = 0
    while True:
        yield i, *ROCK_WH[i], ROCK[i]
        i = (i + 1) % n


def moves(jet_pattern):
    n = len(jet_pattern)
    i, j = 0, 0
    while True:
        if j % 2 == 0:
            yield i, jet_pattern[i]
            i = (i + 1) % n
        else:
            yield None, "V"
        j = (j + 1) % 2


def part1(jet_pattern, stop_cnt, render):
    move_gen = moves(jet_pattern)
    chamber = []
    num_rocks = 0
    for rock_i, w, h, rock in rocks():
        # create rock
        chamber.extend([0] * (3 + h))
        x = 2
        y = len(chamber) - h
        msb = 6 - x
        lsb = msb - w + 1

        # print("new rock:", x, y, msb, lsb, rock)
        # for r, rock_row in enumerate(reversed(rock)):
        #     print(f"{rock_row << lsb:07b}")

        # move rock till stopped
        while True:
            move_idx, move = next(move_gen)
            # print("move:", x, y, msb, lsb, move)
            if move == "<" and msb < 6:
                overlap = 0
                for chamber_row, rock_row in zip(chamber[y : y + h], rock):
                    overlap |= chamber_row & rock_row << (lsb + 1)
                if overlap == 0:
                    x -= 1
            elif move == ">" and lsb > 0:
                overlap = 0
                for chamber_row, rock_row in zip(chamber[y : y + h], rock):
                    overlap |= chamber_row & rock_row << (lsb - 1)
                if overlap == 0:
                    x += 1
            elif move == "V":
                if y == 0:
                    break
                overlap = 0
                for chamber_row, rock_row in zip(chamber[y - 1 : y - 1 + h], rock):
                    overlap |= chamber_row & rock_row << lsb
                if overlap == 0:
                    y -= 1
                else:
                    break

            msb = 6 - x
            lsb = msb - w + 1

            # print("rock:", x, y, msb, lsb)
            # for r, rock_row in enumerate(reversed(rock)):
            #     print(f"{rock_row << lsb:07b}")

        # add stopped rock to chamber
        num_rocks += 1
        msb = 6 - x
        lsb = msb - w + 1
        for r, rock_row in enumerate(rock):
            chamber[y + r] |= rock_row << lsb

        # remove empty top rows from chamber
        while chamber and chamber[-1] == 0:
            del chamber[-1]

        if render:
            # clear screen: https://en.wikipedia.org/wiki/ANSI_escape_code
            print("\033[2J")

            print("chamber:", x, y, msb, lsb)
            for c, chamber_row in enumerate(reversed(chamber)):
                if c < 40:
                    row = "".join(".#"[int(b)] for b in f"{chamber_row:07b}")
                    print(row)
            time.sleep(1)

        if num_rocks == stop_cnt:
            break

    return len(chamber)


def part2(jet_pattern, stop_target, render):
    # For part 2 stop_target being large (1e12), direct simulation is impossible.
    # We rely on periodicity of input to hopefully find a periodicity in output.
    move_gen = moves(jet_pattern)
    move_idx, move = next(move_gen)
    chamber = []
    stop_cnt = 0
    bottom_h = 0
    states = {}
    heights = {}
    for rock_i, rock_w, rock_h, rock in rocks():
        # find the period and height change every period
        state = tuple(chamber) + (rock_i, move_idx)
        height = bottom_h + len(chamber)
        if state in states:
            stop_cnt0 = states[state]
            period = stop_cnt - stop_cnt0
            delta_height = height - heights[stop_cnt0]
            # print(f"stop_cnt={stop_cnt:3d} height={height:4d} state={state}", end=" ")
            # print(f"repeat of: {stop_cnt0:3d}", end=" ")
            # print(f"{period=}, {delta_height=}")
            div_cnt = (stop_target - stop_cnt0) // period
            mod_cnt = (stop_target - stop_cnt0) % period
            chamber_h = div_cnt * delta_height + heights[stop_cnt0 + mod_cnt]
            return chamber_h
        else:
            # print(f"stop_cnt={stop_cnt:3d} height={height:4d} state={state}")
            states[state] = stop_cnt
            heights[stop_cnt] = height

        if stop_cnt == stop_target:
            break

        # create rock
        chamber.extend([0] * (3 + rock_h))
        x = 2
        y = len(chamber) - rock_h
        msb = 6 - x
        lsb = msb - rock_w + 1

        # print("new rock:", x, y, msb, lsb, rock)
        # for r, rock_row in enumerate(reversed(rock)):
        #     print(f"{rock_row << lsb:07b}")

        # move rock till stopped
        stopped = False
        while not stopped:
            # print("move:", x, y, msb, lsb, move)
            if (
                move == "<"
                and msb < 6
                and not any(
                    rock[r] << (lsb + 1) & chamber[y + r] for r in range(len(rock))
                )
            ):
                x -= 1
            elif (
                move == ">"
                and lsb > 0
                and not any(
                    rock[r] << (lsb - 1) & chamber[y + r] for r in range(len(rock))
                )
            ):
                x += 1
            elif move == "V" and y > 0:
                if any(rock[r] << lsb & chamber[y + r - 1] for r in range(len(rock))):
                    stopped = True
                else:
                    y -= 1
            elif move == "V" and y == 0:
                stopped = True

            msb = 6 - x
            lsb = msb - rock_w + 1

            # print("rock:", x, y, msb, lsb)
            # for r, rock_row in enumerate(reversed(rock)):
            #     print(f"{rock_row << lsb:07b}")

            move_idx, move = next(move_gen)

        # add stopped rock to chamber
        stop_cnt += 1
        msb = 6 - x
        lsb = msb - rock_w + 1
        for r, rock_row in enumerate(rock):
            chamber[y + r] |= rock_row << lsb

        # remove empty top rows and bottom unreachable rows from chamber
        bottom = 0
        top = len(chamber) - 1
        found_top = found_bottom = False
        # print(bottom, top, chamber)
        for c in range(len(chamber) - 1, -1, -1):
            if found_top and found_bottom:
                break
            found_top = chamber[c] != 0
            if not found_top:
                top = c
            found_bottom = chamber[c] == 0x7F
            if found_bottom:
                bottom = c
            # print(c, chamber[c], top, bottom, mask)

        bottom_h += bottom
        chamber = chamber[bottom:top]
        chamber = chamber[:top]
        # print(bottom, top, chamber)

        if render:
            # clear screen: https://en.wikipedia.org/wiki/ANSI_escape_code
            print("\033[2J")

            print("chamber:", bottom_h, len(chamber))
            for c, chamber_row in enumerate(reversed(chamber)):
                if c < 40:
                    row = "".join(".#"[int(b)] for b in f"{chamber_row:07b}")
                    print(row)
            time.sleep(1 / 10.0)

    return bottom_h + len(chamber)


def main():
    if len(sys.argv) == 1:
        input_file = "input.txt"
    else:
        input_file = sys.argv[1]

    jet_pattern = pathlib.Path(input_file).read_text().strip()

    print("part 1:", part1(jet_pattern, 2022, render=False))
    print("part 1 (2):", part2(jet_pattern, 2022, render=False))
    print("part 2:", part2(jet_pattern, int(1e12), render=False))


if __name__ == "__main__":
    main()
