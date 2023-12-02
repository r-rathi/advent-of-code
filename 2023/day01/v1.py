"""Day 1: Trebuchet?!"""

import argparse
import pathlib
import re

RE_DIGIT = re.compile(r"\d")
# NB: lookahead assertion (?=...) is used to handle overlapping matches, e.g. eightwo
RE_DIGIT_WORD = re.compile(
    r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", re.IGNORECASE
)
WORD_TO_DIGIT = dict(
    one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9
)


def parse_digit(s):
    try:
        return int(s)
    except ValueError:
        return int(WORD_TO_DIGIT[s])


def find_digits(line, spelled_digits=False):
    if spelled_digits:
        return [parse_digit(s) for s in (RE_DIGIT_WORD.findall(line))]
    else:
        return [parse_digit(s) for s in (RE_DIGIT.findall(line))]


def cal(lines, spelled_digits=False):
    cal_values = []
    for line in lines:
        digits = find_digits(line, spelled_digits=spelled_digits)
        cal_val = 10 * digits[0] + digits[-1] if digits else 0
        # print(line, digits, cal_val)
        cal_values.append(cal_val)
    return sum(cal_values)


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", cal(lines, spelled_digits=False))
    print("part 2:", cal(lines, spelled_digits=True))


if __name__ == "__main__":
    main()
