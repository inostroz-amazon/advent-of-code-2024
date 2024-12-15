import logging
from argparse import ArgumentParser
from typing import List, Tuple, Dict, Set, Optional


class Path:
    def __init__(self, width: int):
        self.width = width
        self.positions: List[int] = list()

    def add(self, position: Tuple[int, int]) -> 'Path':
        x, y = position
        path = Path(self.width)
        path.positions = [y * self.width + x] + self.positions
        return path

    def __str__(self) -> str:
        return '->'.join([f'{position}' for position in self.positions])

    def __repr__(self) -> str:
        return str(self)

def read_input(filename: str) -> List[List[int]]:
    with open(filename) as file:
        return [[int(cell) for cell in list(line.strip())] for line in file.readlines()]

def is_within_bounds(matrix: List[List[int]], position: Tuple[int, int]) -> bool:
    x, y = position
    return 0 <= y < len(matrix) and 0 <= x < len(matrix[0])

def dfs(
        matrix: List[List[int]],
        position: Tuple[int, int],
        score: Dict[Tuple[int, int], Set[Tuple[int, int]]],
        rating: Dict[Tuple[int, int], List[Path]],
) -> Tuple[Set[Tuple[int, int]], List[Path]]:
    if position in score:
        return score[position], rating[position]
    x, y = position
    if matrix[y][x] == 9:
        score[position] = {(x, y)}
        rating[position] = [Path(len(matrix[0])).add((x, y))]
        return score[position], rating[position]
    directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
    the_sum = set()
    the_paths = []
    for dx, dy in directions:
        new_x = x + dx
        new_y = y + dy
        if is_within_bounds(matrix, (new_x, new_y)) and matrix[y][x] + 1 == matrix[new_y][new_x]:
            pos_score, pos_rating = dfs(matrix, (new_x, new_y), score, rating)
            the_sum = the_sum.union(pos_score)
            for path in pos_rating:
                the_paths.append(path.add((x, y)))

    score[position] = the_sum
    rating[position] = the_paths
    return score[position], rating[position]


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    matrix = read_input(args.input)
    score = dict()
    rating = dict()
    the_sum = 0
    the_paths = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                pos_sum, pos_paths = dfs(matrix, (x, y), score, rating)
                the_sum += len(pos_sum)
                the_paths += len(set([str(path) for path in pos_paths]))
    logging.info(f' {the_sum}')
    logging.info(f' {the_paths}')
