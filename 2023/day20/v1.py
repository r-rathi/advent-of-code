"""Day 20: Pulse Propagation"""

import argparse
import math
import pathlib
from collections import deque
from functools import reduce
from math import prod
from operator import and_


verbose: bool = False


class Module:
    def __init__(self, name: str, dsts: list[str]):
        self.name = name
        self.dsts = dsts
        self.srcs: list[str] = []
        self.cnwk: CableNetwork | None = None

    def __repr__(self):
        cls = self.__class__.__name__
        srcs = ", ".join(self.srcs)
        dsts = ", ".join(self.dsts)
        return f"{cls}({self.name:}, [{srcs}], [{dsts}])"

    def reset(self):
        pass

    def receive(self, src: str, pulse: bool):
        for dst in self.dsts:
            self.cnwk.send(self.name, dst, pulse)


class Broadcast(Module):
    pass


class Sink(Module):
    pass


class Flop(Module):
    def __init__(self, name: str, dsts: list[str]):
        super(Flop, self).__init__(name, dsts)
        self.state: bool = False

    def reset(self):
        self.state = False

    def receive(self, src: str, pulse: bool):
        if not pulse:
            self.state = not self.state
            super(Flop, self).receive(src, self.state)


class Nand(Module):
    def __init__(self, name: str, dsts: list[str]):
        super(Nand, self).__init__(name, dsts)
        self.received: dict[str, bool] = {}

    def reset(self):
        self.received = {}

    def receive(self, src: str, pulse: bool):
        self.received[src] = pulse
        nand = not reduce(and_, (self.received.get(src, False) for src in self.srcs))
        super(Nand, self).receive(src, nand)


class CableNetwork:
    def __init__(self):
        self.modules: dict[str, Module] = {}
        self.cycle = 0
        self.pulses = deque()
        self.pulse_count = [0, 0]
        self.trace = None  # Callback function

    def reset(self):
        for module in self.modules.values():
            module.reset()
        self.cycle = 0
        self.pulses.clear()
        self.pulse_count = [0, 0]

    def add_module(self, module: Module):
        module.cnwk = self
        self.modules[module.name] = module

    def connect(self):
        sink_modules = []

        for name, module in self.modules.items():
            for dst in module.dsts:
                if dst not in self.modules:
                    dst_module = Sink(dst, [])
                    sink_modules.append(dst_module)
                else:
                    dst_module = self.modules[dst]
                dst_module.srcs.append(name)

        for module in sink_modules:
            self.add_module(module)

    def send(self, src: str, dst: str, pulse: bool):
        self.pulse_count[pulse] += 1
        self.pulses.append((src, dst, pulse))

        if self.trace is not None:
            self.trace(self.cycle, src, dst, pulse)

        if verbose:
            p = "-high->" if pulse else "-low->"
            print(src, p, dst)

    def propage_pulses(self):
        while self.pulses:
            src, dst, pulse = self.pulses.popleft()
            self.modules[dst].receive(src, pulse)

    def push_button(self):
        self.cycle += 1
        self.send("button", "broadcaster", False)
        self.propage_pulses()


def part1(cable_network: CableNetwork) -> int:
    for _ in range(1000):
        cable_network.push_button()

    # print("Pulse count:", cables.pulse_count)
    return prod(cable_network.pulse_count)


def part2(cable_network: CableNetwork, output="rx") -> int:
    # Solving this part relies on the fact that the given cable network is
    # actually composed of independent FSMs with periods, say T0, T1, ...
    # The output pulses of these FSMs are then NANDed together to create
    # the final output "rx". The answerd is then LCM(T0, T1, ...).

    # Find the NAND gate driving the output
    sink = cable_network.modules[output]
    assert len(sink.srcs) == 1, sink
    nand = cable_network.modules[sink.srcs[0]]

    # Look for high input pulses coming in to the NAND gate and compute periods.
    prev_cycle = {src: 0 for src in nand.srcs}
    periods = {src: [] for src in nand.srcs}

    def trace(cycle, src, dst, pulse):
        if not (dst == nand.name and pulse):
            return
        period = cycle - prev_cycle[src]
        prev_cycle[src] = cycle
        periods[src].append(period)
        # print(cycle, src, period)

    cable_network.trace = trace

    for _ in range(10**4):
        cable_network.push_button()
        # Make sure last two periods are same
        if any(len(ps) < 2 for ps in periods.values()):
            continue
        if all(ps[-1] == ps[-2] for ps in periods.values()):
            break

    # print(periods)

    return math.lcm(*(ps[-1] for ps in periods.values()))


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-v", action="store_true", help="verbose")
    args = parser.parse_args()

    global verbose
    verbose = args.v

    lines = pathlib.Path(args.f).read_text().splitlines()

    cable_network = CableNetwork()
    for line in lines:
        if line.startswith("#"):
            continue
        mod, dsts = line.split(" -> ")
        dsts = dsts.split(", ")
        if mod == "broadcaster":
            module = Broadcast(mod, dsts)
        elif mod[0] == "%":
            module = Flop(mod[1:], dsts)
        elif mod[0] == "&":
            module = Nand(mod[1:], dsts)
        else:
            raise ValueError(f"unknown module: {mod}")
        cable_network.add_module(module)
    cable_network.connect()

    # for module in cable_network.modules.values():
    #     print(module)

    print("part 1:", part1(cable_network))

    cable_network.reset()
    outputs = [n for n, m in cable_network.modules.items() if isinstance(m, Sink)]
    if outputs:
        print("part 2:", part2(cable_network, outputs[0]))
    else:
        print("part 2:", "skipped")


if __name__ == "__main__":
    main()
