import logging
import re
from argparse import ArgumentParser
from typing import List


class Statement:
    def __init__(self, result: int, operands: List[int]):
        self.result = result
        self.operands = operands

    def __str__(self) -> str:
        return f'{self.result}: {self.operands}'

    @staticmethod
    def from_str(line: str) -> 'Statement':
        parts = line.split(':')
        return Statement(int(parts[0]), list(map(int, re.findall(r'\d+', parts[1]))))

def parse_input(filename: str) -> List[Statement]:
    with open(filename) as file:
        return [Statement.from_str(line) for line in file.readlines()]

def is_valid_statement(statement: Statement) -> bool:
    if not statement.operands:
        return not statement.result
    sum_result = statement.result - statement.operands[-1]
    sum_statement = Statement(sum_result, statement.operands[:-1])
    if is_valid_statement(sum_statement):
        return True
    if not statement.result % statement.operands[-1]:
        mult_statement = Statement(int(statement.result / statement.operands[-1]), statement.operands[:-1])
        if is_valid_statement(mult_statement):
            return True
    if statement.result < 0 or not str(statement.result).endswith(str(statement.operands[-1])):
        return False
    new_result = int(str(statement.result)[:-len(str(statement.operands[-1]))])
    concat_statement = Statement(new_result, statement.operands[:-1])
    if is_valid_statement(concat_statement):
        return True
    else:
        return False

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    statements = parse_input(args.input)
    test_values = sum([statement.result for statement in statements if is_valid_statement(statement)])
    logging.info(f' {test_values}')
