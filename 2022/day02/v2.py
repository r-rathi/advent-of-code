"""Day 2: Rock Paper Scissors"""
import pathlib

# Strategy
# C X
# A Y
# ...
lines = pathlib.Path("input.txt").read_text().splitlines()

index = dict(A=0, B=1, C=2, X=0, Y=1, Z=2)
strategy = [[index[s] for s in line.split()] for line in lines]


# plays: rock=0, paper=1, scissors=2
# outcome: loss=0, draw=1, win=2

def plays2outcome(play0, play1):
    return (play1 - play0 + 1) % 3


def outcome2play1(play0, outcome):
    return (outcome + play0 - 1) % 3


shape_score = [1, 2, 3]
outcome_score = [0, 3, 6]

score1 = sum(shape_score[p1] + outcome_score[plays2outcome(p0, p1)] for p0, p1 in strategy)
score2 = sum(shape_score[outcome2play1(p0, oc)] + outcome_score[oc] for p0, oc in strategy)

print("part 1:", score1)
print("part 2:", score2)
