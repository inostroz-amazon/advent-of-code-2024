import logging
from argparse import ArgumentParser
from typing import Dict, List, NoReturn, Set, Tuple


def get_middle(line: str, dependency_dict: Dict[int, Set[int]]) -> Tuple[int, bool]:
    pages = [int(v) for v in line.split(',')]
    printed = set()
    pages_set = set(pages)
    fixed = False
    i = 0
    while i < len(pages):
        dependencies = dependency_dict.get(pages[i], set())
        subdeps = pages_set & dependencies
        if subdeps <= printed:
            printed.add(pages[i])
            i += 1
        else:
            missing_dependencies = subdeps - printed
            for dependency in missing_dependencies:
                pages.remove(dependency)
                pages.insert(i, dependency)
            fixed = True
    middle_index = int((len(pages) - 1) / 2)
    return pages[middle_index], fixed


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    dependency_dict = dict()
    dependency_built = False
    the_sum_part_1 = 0
    the_sum_part_2 = 0
    with open(args.input) as file:
        for line in file.readlines():
            line = line.strip()
            if not line:
                dependency_built = True
            elif dependency_built:
                middle, fixed = get_middle(line, dependency_dict)
                if not fixed:
                    the_sum_part_1 += middle
                else:
                    the_sum_part_2 += middle
            else:
                pair = [int(v) for v in line.split('|')]
                dependencies = dependency_dict.get(pair[1], set())
                dependencies.add(pair[0])
                dependency_dict[pair[1]] = dependencies
    logging.info(the_sum_part_1)
    logging.info(the_sum_part_2)
