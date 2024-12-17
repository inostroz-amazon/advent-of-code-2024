import logging
import re
from argparse import ArgumentParser
from typing import List, Dict


def read_input(filename: str) -> List[str]:
    with open(filename) as file:
        return list(re.findall(r'\d+', file.readline()))


def recursive_blink(value: str, level: int, cache: Dict[str, int]) -> int:
    if level == 0:
        return 1
    key = f'{value}#{level}'
    if key in cache:
        return cache[key]

    child_nodes = []
    if value == "0":
        child_nodes.append("1")
    elif len(value) % 2 == 0:
        half = int(len(value) / 2)
        child_nodes.append(value[:half])
        child_nodes.append(str(int(value[half:])))
    else:
        child_nodes.append(str(int(value) * 2024))
    cache[key] = sum([recursive_blink(child_value, level - 1, cache) for child_value in child_nodes])
    return cache[key]


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    stones = read_input(args.input)
    cache = dict()
    values = [recursive_blink(stone, 75, cache) for stone in stones]
    count = sum(values)
    logging.info(f' {count}')
