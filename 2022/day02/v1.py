"""Day 2: Rock Paper Scissors"""

# Scoring
# rock (0) < paper (1)
# paper (1) < scissors (2)
# scissors (2) < rock (0)
# loss = 0, draw = 1, win = 2
outcome = [
    [1, 2, 0],
    [0, 1, 2],
    [2, 0, 1]
]
shape_score = [1, 2, 3]
outcome_score = [0, 3, 6]

# Strategy
# C X
# A Y
# ...
with open("input.txt", "r") as f:
    lines = f.readlines()

indices = dict(A=0, B=1, C=2, X=0, Y=1, Z=2)


def str_to_indices(s):
    a, x = s.split()
    ai, xi = indices[a], indices[x]
    return ai, xi


strategy = [str_to_indices(line) for line in lines]


score = sum(shape_score[xi] + outcome_score[outcome[ai][xi]] for ai, xi in strategy)
print("part 1:", score)


# Reverse the play0 x play1 -> outcome matrix to play0 x outcome -> play1
play = [-1, -1, -1]
for p0 in range(3):
    play[p0] = [-1, -1, -1]
    for p1 in range(3):
        o = outcome[p0][p1]
        play[p0][o] = p1
# print(play)

score = sum(shape_score[play[ai][xi]] + outcome_score[xi] for ai, xi, in strategy)
print("part 2:", score)
