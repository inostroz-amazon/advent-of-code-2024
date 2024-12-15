import logging
from argparse import ArgumentParser
from typing import List, Dict, Tuple, Set


def read_input(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]

def is_satellite(cell: str) -> bool:
    return cell.isalnum()

def generate_satellite_dict(matrix: List[str]) -> Dict[str, Set[Tuple[int, int]]]:
    the_dict = dict()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if is_satellite(matrix[i][j]):
                satellites = the_dict.get(matrix[i][j], set())
                satellites.add((i, j))
                the_dict[matrix[i][j]] = satellites
    return the_dict

def find_antinodes(satellites: Set[Tuple[int, int]], width: int, height: int) -> Set[Tuple[int, int]]:
    the_result = set()
    copy_satellites = satellites.copy()
    while copy_satellites:
        satellite_y, satellite_x = copy_satellites.pop()
        for other_satellite_y, other_satellite_x in copy_satellites:
            the_result.add((satellite_y, satellite_x))
            the_result.add((other_satellite_y, other_satellite_x))
            distance_y = other_satellite_y - satellite_y
            distance_x = other_satellite_x - satellite_x
            s_y = satellite_y
            s_x = satellite_x
            while is_within_bounds((s_y - distance_y, s_x - distance_x), width, height):
                s_y -= distance_y
                s_x -= distance_x
                the_result.add((s_y, s_x))
            s_y = other_satellite_y
            s_x = other_satellite_x
            while is_within_bounds((s_y + distance_y, s_x + distance_x), width, height):
                s_y += distance_y
                s_x += distance_x
                the_result.add((s_y, s_x))
    return the_result

def find_all_antinodes(satellite_dict: Dict[str, Set[Tuple[int, int]]], width: int, height: int) -> Set[Tuple[int, int]]:
    return {position for s, positions in satellite_dict.items() for position in find_antinodes(positions, width, height)}

def is_within_bounds(position: Tuple[int, int], width: int, height: int) -> bool:
    y, x = position
    return 0 <= x < width and 0 <= y < height

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    matrix = read_input(args.input)
    satellite_dict = generate_satellite_dict(matrix)
    antinodes = find_all_antinodes(satellite_dict, len(matrix[0]), len(matrix))
    logging.info(f' {len(antinodes)}')
