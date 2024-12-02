import logging
import re
from argparse import ArgumentParser
from typing import List


def is_increasing(the_numbers: List[int], removed_one: bool = False) -> bool:
    for index in range(len(the_numbers) - 1):
        if the_numbers[index] >= the_numbers[index + 1] or abs(the_numbers[index] - the_numbers[index + 1]) > 3:
            if removed_one:
                return False
            return is_increasing(the_numbers[0:index] + the_numbers[index+1:], True) or is_increasing(the_numbers[0:index+1] + the_numbers[index+2:], True)
    return True


def is_decreasing(the_numbers: List[int], removed_one: bool = False) -> bool:
    for index in range(len(the_numbers) - 1):
        if the_numbers[index] <= the_numbers[index + 1] or abs(the_numbers[index] - the_numbers[index + 1]) > 3:
            if removed_one:
                return False
            return is_decreasing(the_numbers[0:index] + the_numbers[index+1:], True) or is_decreasing(the_numbers[0:index+1] + the_numbers[index+2:], True)
    return True


def is_report_safe(the_numbers: List[int]) -> bool:
    return is_increasing(the_numbers) or is_decreasing(the_numbers)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    with open(args.input) as file:
        count = 0
        for line in file.readlines():
            numbers = list(map(int, re.findall(r'\d+', line)))
            if is_report_safe(numbers):
                logging.info(f'Safe: {numbers}')
                count += 1
        logging.info(f' {count}')


