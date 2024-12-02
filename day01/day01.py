import logging
import re
from argparse import ArgumentParser
from typing import List, Tuple


def read_input(filename: str) -> Tuple[List[int], List[int]]:
    list1 = []
    list2 = []
    with open(filename) as file:
        for line in file.readlines():
            numbers = list(map(int, re.findall(r'\d+', line)))
            list1.append(numbers[0])
            list2.append(numbers[1])
    return list1, list2


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    list1, list2 = read_input(args.input)
    list1.sort()
    list2.sort()
    distance = 0
    similarity_dict = {}
    for value1, value2 in zip(list1, list2):
        distance += abs(value1 - value2)
        similarity_dict[value2] = similarity_dict.get(value2, 0) + 1

    logging.info(f' {distance}')

    similarity = 0
    for value1 in list1:
        similarity += value1 * similarity_dict.get(value1, 0)

    logging.info(f' {similarity}')
