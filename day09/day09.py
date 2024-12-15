import logging
from argparse import ArgumentParser
from typing import List


def build_blocks(disk_map: str) -> List[str]:
    blocks = []
    id = 0
    for i in range(len(disk_map)):
        digit = int(disk_map[i])
        if i % 2:
            blocks += ['.'] * digit
        else:
            blocks += [f'{id}'] * digit
            id += 1
    return blocks

def read_disk_map(filename: str) -> str:
    with open(filename) as file:
        return file.readline()

def defragment_blocks(block_list: List[str]) -> List[str]:
    i = 0
    j = len(block_list) - 1
    while i < j:
        while block_list[i] != '.' and i < j:
            i += 1
        while block_list[j] == '.' and i < j:
            j -= 1
        if i >= j:
            break
        block_list[i] = block_list[j]
        block_list[j] = '.'
    return block_list

def defragment_files(block_list: List[str]) -> List[str]:
    j_end = len(block_list) - 1
    logging.info(f' {block_list}')
    while j_end >= 0:
        while j_end > 0 and block_list[j_end] == '.':
            j_end -= 1
        j_start = j_end
        while j_start >= 0 and block_list[j_start] == block_list[j_end]:
            j_start -= 1
        file_size = j_end - j_start
        i_start = 0
        while i_start <= j_start:
            while i_start <= j_start and block_list[i_start] != '.':
                i_start += 1
            i_end = i_start
            while i_end <= j_start and block_list[i_end] == '.':
                i_end += 1
            space_available = i_end - i_start
            if space_available >= file_size:
                for x in range(i_start, i_start + file_size):
                    block_list[x] = block_list[j_end]
                for x in range(j_start + 1, j_end + 1):
                    block_list[x] = '.'
                logging.info(f' {block_list}')
                break
            i_start = i_end
        j_end = j_start
    return block_list

def checksum(block_list: List[str]) -> int:
    return sum([int(block_list[i]) * i for i in range(len(block_list)) if block_list[i].isdigit()])

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    disk_map = read_disk_map(args.input)
    blocks = defragment_blocks(build_blocks(disk_map))
    logging.info(f' {checksum(blocks)}')
    blocks = defragment_files(build_blocks(disk_map))
    logging.info(f' {checksum(blocks)}')
