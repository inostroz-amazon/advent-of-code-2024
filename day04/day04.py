import logging
from argparse import ArgumentParser
from typing import List, Tuple


def read_input(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def find_word(word: str, matrix: List[str], location: Tuple[int, int], direction: Tuple[int, int]) -> bool:
    x, y = location
    rows_length = len(matrix)
    column_length = len(matrix[0])
    if x < 0 or x >= rows_length or y < 0 or y >= column_length:
        return False
    if len(word) == 1:
        return matrix[x][y] == word
    if matrix[x][y] != word[0]:
        return False
    dx, dy = direction
    return find_word(word[1:], matrix, (x + dx, y + dy), direction)


def count_x(matrix: List[str]) -> int:
    count = 0
    for x in range(1, len(matrix) - 1):
        for y in range(1, len(matrix[0]) - 1):
            if matrix[x][y] == 'A':
                word1 = matrix[x - 1][y - 1] + 'A' + matrix[x + 1][y + 1]
                word2 = matrix[x + 1][y - 1] + 'A' + matrix[x - 1][y + 1]
                if word1 in {'MAS', 'SAM'} and word2 in {'MAS', 'SAM'}:
                    count += 1
    return count


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    matrix = read_input(args.input)
    rows_length = len(matrix)
    column_length = len(matrix[0])
    count = 0
    directions = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
    ]
    for row in range(rows_length):
        for column in range(column_length):
            for direction in directions:
                if find_word('XMAS', matrix, (row, column), direction):
                    count += 1
    logging.info(f' {count}')
    logging.info(f' {count_x(matrix)}')
