from typing import Optional, Generator
from pathlib import Path


def decode_line(line: str, word_correction: bool) -> Optional[int]:
    """Decode the calibration string into a calibration number, with optional word correction.
    If no numbers are detected, will return None.

    Calibration numbers are two digit numbers comprised of the first and last numbers of a string
    in that order. For example

    >>> decode_line("1abc2", False)
    12
    >>> decode_line("pqr3stu8vwx", False)
    38
    >>> decode_line("a1b2c3d4e5f", False)
    15
    >>> decode_line("treb7uchet", False)
    77

    If you enable word_correction, then spelled words will count as well.
    >>> decode_line("two1nine", True)
    29
    >>> decode_line("eightwothree", True)
    83
    >>> decode_line("abcone2threexyz", True)
    13
    >>> decode_line("xtwone3four", True)
    24
    >>> decode_line("4nineeightseven2", True)
    42
    >>> decode_line("zoneight234", True)
    14
    >>> decode_line("7pqrstsixteen", True)
    76
    >>> decode_line("2threerjnineonev", True)
    21

    :param line: The calibration string to decode into a calibration number.
    :param word_correction: Whether to count spelled numbers (e.g.: "three") as numbers.
    :return: Calibration number, or None if invalid calibration string.
    """

    word_numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    first_num: Optional[int] = None
    last_num: Optional[int] = None

    numbers = [str(number) for number in range(10)]

    for i in range(len(line)):
        left_cursor = line[i]
        right_cursor = line[-(i+1)]
        
        if first_num is None and left_cursor in numbers:
            first_num = int(left_cursor)

        if last_num is None and right_cursor in numbers:
            last_num = int(right_cursor)

        if word_correction:
            for number, word_number in enumerate(word_numbers):
                left_word = line[i:i+len(word_number)]

                if i == 0:
                    right_word = line[-len(word_number):]
                else:
                    right_word = line[-(i+len(word_number)+1):-i]

                if first_num is None and word_number in left_word:
                    first_num = number + 1

                if last_num is None and word_number in right_word:
                    last_num = number + 1

                if first_num is not None and last_num is not None:
                    break

        if first_num is not None and last_num is not None:
            break

    if first_num is None and last_num is None:
        return None
    elif first_num is None:
        return int(f"{last_num}{last_num}")
    elif last_num is None:
        return int(f"{first_num}{first_num}")
    else:
        return int(f"{first_num}{last_num}")


def sum_lines(in_path: Path, word_correction: bool) -> int:
    total = 0

    for line in open(in_path):
        decoded_line = decode_line(line.strip(), word_correction)
        print(line.strip(), decoded_line)
        total += decoded_line

    return total


if __name__ == "__main__":
    import doctest
    import argparse
    doctest.testmod()

    parser = argparse.ArgumentParser(prog='d1',
                    description="Decodes data from Advent of Code '23, Day 1")
    parser.add_argument('-i', '--infile', default='in/d1.txt', type=Path)
    parser.add_argument('-w', '--wordcorrection', default=False, type=bool)

    args = parser.parse_args()

    print("CALIBRATION VALUE:", sum_lines(args.infile, args.wordcorrection))