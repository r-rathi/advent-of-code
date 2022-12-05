#!/usr/bin/env python

"""Download the puzzle input for given year and day"""
import argparse

import requests

INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"


def download(url, file, cookie):
    response = requests.get(url, headers={"Cookie": cookie})

    if response.status_code == 200:
        with open(file, "w") as f:
            f.write(response.text)
    else:
        print(f"Failed to download file: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(
        description="Download the input for an Advent of Code puzzle"
    )
    parser.add_argument("-c", "--session-cookie", required=True)
    parser.add_argument("-y", "--year", type=int, required=True)
    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-f", "--file", required=True)

    args = parser.parse_args()

    url = INPUT_URL.format(year=args.year, day=args.day)
    cookie = "session=" + args.session_cookie

    download(url=url, file=args.file, cookie=cookie)


if __name__ == "__main__":
    main()
