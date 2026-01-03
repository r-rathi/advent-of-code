"""Day 10: Factory

This puzzle can be formulated as an integer linear programming of the form:
    find x that minimizes:
        c^T @ x
    subject to constraints:
        A @ x = b (mod-2 for Part 1)
        x >= 0
        x integer

Given m lights/joltages and n buttons, we have:
- A with shape (m, n), where A[i, j] = 1 if button j connects to light/joltage i.
- b with length m specifies the m light/joltage requirements
- x with length n is the number of presses of each button
- c with length n is all-ones, resulting in the cost functions being sum(x),
  i.e. we minimize the total number of presses

I brute forced part 1 using exhaustive search of all 2^n n-bit vectors. For part 2,
I used this as an excuse to learn how to use the SciPy milp library.

References:
- https://en.wikipedia.org/wiki/Integer_programming
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html

Tags: #ilp #milp #integer-linear-programming
"""

from itertools import product
from typing import NamedTuple

import numpy as np
from scipy import optimize


class Machine(NamedTuple):
    buttons: np.ndarray
    lights: np.ndarray
    joltages: np.ndarray


def exhaustive_solution(A: np.ndarray, b: np.ndarray) -> int:
    """
    Minimize sum(x) such that A @ x = b mod-2, x in {0, 1}
    Returns the minimum sum(x)
    """
    m, n = A.shape
    return min(sum(x) for x in product(range(2), repeat=n) if np.all((A @ x) % 2 == b))


def ilp_solution(A: np.ndarray, b: np.ndarray) -> int:
    """
    Minimize sum(x) such that A @ x = b, x >= 0
    Returns the minimum sum(x)
    """
    m, n = A.shape
    c = np.ones(n)
    constraints = optimize.LinearConstraint(A, b, b)
    integrality = np.ones_like(c)
    # noinspection PyTypeChecker
    res = optimize.milp(c=c, constraints=constraints, integrality=integrality)
    return int(res.fun)


def part1(machines: list[Machine]) -> int:
    return sum(exhaustive_solution(m.buttons, m.lights) for m in machines)


def part2(machines: list[Machine]) -> int:
    return sum(ilp_solution(m.buttons, m.joltages) for m in machines)


def main():
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    machines: list[Machine] = []
    for line in lines:
        light_spec, *button_connections, joltage_spec = line.split(" ")

        lights = np.array([c == "#" for c in light_spec[1:-1]], dtype=np.uint8)
        joltages = np.array([int(x) for x in joltage_spec[1:-1].split(",")])

        buttons = np.zeros((len(lights), len(button_connections)), dtype=np.uint8)
        for button, connections in enumerate(button_connections):
            for connection in map(int, connections[1:-1].split(",")):
                buttons[connection, button] = 1

        machines.append(Machine(buttons, lights, joltages))

    print("part 1:", part1(machines))
    print("part 2:", part2(machines))


if __name__ == "__main__":
    main()
