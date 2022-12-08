"""Day 6: Tuning Trouble"""
import pathlib

input = pathlib.Path("input.txt").read_text()


def get_marker_pos(signal, marker_size):
    for pos in range(len(signal)):
        block = signal[pos:pos + marker_size]
        if len(set(block)) == marker_size:
            return pos
    raise IndexError("marker not found")


start_of_packet = get_marker_pos(input, 4) + 4
start_of_message = get_marker_pos(input, 14) + 14

print("part 1:", start_of_packet)
print("part 2:", start_of_message)
