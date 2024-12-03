import logging
import re
from argparse import ArgumentParser

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    with open(args.input) as file:
        line = file.read()
        matches = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)', line)
        result = 0
        should_add = True
        for match in matches:
            full_match = match.group(0)
            if full_match == "do()":
                should_add = True
            elif full_match == "don't()":
                should_add = False
            elif should_add:
                x = int(match.group(1))
                y = int(match.group(2))
                result += x * y
        logging.info(f' {result}')
