import logging
from argparse import ArgumentParser
from typing import List, NoReturn, Tuple

DIRECTIONS = {'^', 'v', '<', '>'}


def _next_direction(direction: str) -> str:
    if direction == '^':
        return '>'
    elif direction == '>':
        return 'v'
    elif direction == 'v':
        return '<'
    else:
        return '^'


def _get_direction_step(direction: str) -> Tuple[int, int]:
    if direction == '^':
        return -1, 0
    if direction == '>':
        return 0, 1
    if direction == 'v':
        return 1, 0
    return 0, -1


class Floor:
    def __init__(self, matrix: List[List[str]]):
        self.original_matrix = matrix
        self.matrix = [row.copy() for row in self.original_matrix]
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
        self.direction = '^'

    def calculate(self) -> Tuple[int, int]:
        guard_x, guard_y = self.get_start_position()
        x = guard_x
        y = guard_y
        self.direction = self.matrix[x][y]
        start_direction = self.direction
        path = set()
        count = 1
        while self._is_within_bound(x, y):
            if self.matrix[x][y] not in DIRECTIONS:
                count += 1
            self.matrix[x][y] = self.direction
            if (x, y) != (guard_x, guard_y):
                path.add((x, y))
            dx, dy = _get_direction_step(self.direction)
            if self._is_within_bound(x + dx, y + dy) and self._is_obstacle(x + dx, y + dy):
                self.direction = _next_direction(self.direction)
                continue
            x += dx
            y += dy

        loops = 0
        for cell_x, cell_y in path:
            matrix_copy = [row.copy() for row in self.original_matrix]
            matrix_copy[cell_x][cell_y] = '#'
            if self._check_for_loop(matrix_copy, guard_x, guard_y, start_direction):
                loops += 1
        return count, loops

    def _check_for_loop(self, matrix: List[List[str]], x: int, y: int, direction: str) -> bool:
        path = set()
        while self._is_within_bound(x, y):
            if (x, y, direction) in path:
                return True
            path.add((x, y, direction))
            dx, dy = _get_direction_step(direction)
            if self._is_within_bound(x + dx, y + dy) and matrix[x + dx][y + dy] == '#':
                direction = _next_direction(direction)
                continue
            x += dx
            y += dy
        return False

    def _is_within_bound(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def _is_obstacle(self, x: int, y: int) -> bool:
        return self.matrix[x][y] == '#'

    def get_start_position(self) -> Tuple[int, int]:
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] in DIRECTIONS:
                    return i, j
        raise ValueError('No start position found')

    def print_matrix(self) -> NoReturn:
        lines = [''.join(characters) for characters in self.matrix]
        for line in lines:
            logging.info(f' {line}')

    def print_original_matrix(self) -> NoReturn:
        lines = [''.join(characters) for characters in self.original_matrix]
        for line in lines:
            logging.info(f' {line}')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    matrix = []
    with open(args.input) as file:
        for line in file.readlines():
            line = line.strip()
            matrix.append(list(line))
    floor = Floor(matrix)
    x, y = floor.get_start_position()
    logging.info(f' {floor.calculate()}')
