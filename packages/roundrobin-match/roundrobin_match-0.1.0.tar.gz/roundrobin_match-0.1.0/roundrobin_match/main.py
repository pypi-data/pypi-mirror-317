import sys
import argparse
import random
from collections import defaultdict
from typing import TypeAlias


Match: TypeAlias = tuple[int, int]
Matches: TypeAlias = list[Match]
Schedule: TypeAlias = list[Matches]


class RoundRobinScheduleException(Exception):
    def __init__(self, message) -> None:
        self.message = message


def round_robin_schedule(size: int, shuffle: bool = False) -> Schedule:
    schedule: Schedule = []
    participants: list[int] = list(range(0, size))

    if shuffle:
        random.shuffle(participants)

    for _ in range(size - 1):
        matches: Matches = []

        for index in range(size // 2):
            matches.append((participants[index], participants[-index - 1]))

        schedule.append(matches)

        participants = [participants[0]] + participants[-1:] + participants[1:-1]

    valid, message = _validate_round_robin_schedule(schedule=schedule, size=size)
    if not valid:
        raise RoundRobinScheduleException(message=message)
    return schedule


def _show_results(names: list[str], schedule: Schedule):
    data = {}
    for i, round_matches in enumerate(schedule):
        data[i] = [(names[a], names[b]) for a, b in round_matches]

    header = "| DAY | " + " | ".join(names) + " |"
    separator = "| ---- | " + "|".join(["-" * (len(name) + 2) for name in names]) + "|"

    rows = []
    for round_name, pairs in data.items():
        row = [""] * len(names)
        for first, second in pairs:
            row[names.index(first)] = second
            row[names.index(second)] = first
        rows.append(f"| {round_name} | " + " | ".join(row) + "|")
    table = "\n".join([header, separator] + rows)
    print(table)


def _validate_round_robin_schedule(schedule: Schedule, size: int) -> tuple[bool, str]:
    match_count: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    if size % 2 == 1:
        return False, f"{size} is odd value."

    if len(schedule) != size - 1:
        return False, f"{schedule} is not valid size."

    if not all(len(matches) == (size // 2) for matches in schedule):
        return False, f"{schedule} is not valid size"

    # check the row
    for matches in schedule:
        seen: set[int] = set()
        for a, b in matches:
            if not (0 <= a < size):
                return (
                    False,
                    f"{a} is invalid order. the size is {size}.\n debug: {schedule}",
                )
            if not (0 <= b < size):
                return (
                    False,
                    f"{b} is invalid order. the size is {size}.\n debug: {schedule}",
                )
            match_count[a][b] += 1
            match_count[b][a] += 1
            seen.add(a)
            seen.add(b)

        if len(seen) != size:
            return False, f"{seen} is invalid size."

    # check the all match
    for d in match_count.values():
        if not all(count == 1 for count in d.values()):
            return False, f"{d} is invalid match size."
    return True, ""


def _parse_args() -> tuple[int, list[str]]:
    parser = argparse.ArgumentParser(
        description="A cli to execute round robin matching.",
        usage="roundrobin_match --seed <INTEGER> --list <ITEM1> <ITEM2> ...",
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=-1,
        help="Seed value (integer). if you add a seed, the output is shuffled.",
    )
    parser.add_argument(
        "--list", nargs="+", type=str, required=True, help="List of values."
    )

    args = parser.parse_args()
    return args.seed, args.list


def main() -> None:
    seed, names = _parse_args()
    shuffle = False
    size = len(names)

    if seed >= 0:
        shuffle = True
        random.seed(seed)

    if size % 2 == 1:
        size += 1
        names.append("break")

    try:
        _show_results(names, round_robin_schedule(size, shuffle))
    except RoundRobinScheduleException as err:
        print(err.message, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
