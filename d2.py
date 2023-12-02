from typing import Any, Tuple, Union
from collections.abc import Iterable
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DiceGroup:
    """
    Represents a collection of blue, green, and red dice.

    It's primary use is comparing whether one dice group is a subset of the other
    >>> bag = DiceGroup(10, 20, 30)
    >>> sample = DiceGroup(2, 2, 3)
    >>> (bag > sample, bag < sample)
    (True, False)

    You can also determine the "power" of a group of cubes
    >>> sample.power()
    12

    :param num_blue: Number of blue dice
    :param num_green: Number of green dice
    :param num_red: Number of red dice
    """
    num_blue: int
    num_green: int
    num_red: int

    def __eq__(self, other: Any) -> bool:
        match other:
            case DiceGroup(_, _, _):
                return ((self.num_blue == other.num_blue) and (self.num_green == other.num_green) and
                        (self.num_red == other.num_red))
            case _:
                raise NotImplementedError("Bags can only be compared with games and other bags")

    def __gt__(self, other) -> bool:
        match other:
            case DiceGroup(_, _, _):
                return ((self.num_blue > other.num_blue) or (self.num_green > other.num_green) or
                        (self.num_red > other.num_red))
            case _:
                raise NotImplementedError("Bags can only be compared with games and other bags")

    def __lt__(self, other) -> bool:
        match other:
            case DiceGroup(_, _, _):
                return ((self.num_blue < other.num_blue) or (self.num_green < other.num_green) or
                        (self.num_red < other.num_red))
            case _:
                raise NotImplementedError("Bags can only be compared with games and other bags")

    def __ge__(self, other) -> bool:
        match other:
            case DiceGroup(_, _, _):
                return (self > other) or (self == other)
            case _:
                raise NotImplementedError("Bags can only be compared with games and other bags")

    def __le__(self, other) -> bool:
        match other:
            case DiceGroup(_, _, _):
                return (self < other) or (self == other)
            case _:
                raise NotImplementedError("Bags can only be compared with games and other bags")

    def power(self) -> int:
        return self.num_red * self.num_blue * self.num_green


def max_dice_group(groups: Iterable[DiceGroup]) -> DiceGroup:
    """
    Returns a dice group with the maximum number of dice of each colour.

    >>> group1 = DiceGroup(10, 1, 2)
    >>> group2 = DiceGroup(5, 3, 4)
    >>> max_dice_group([group1, group2])
    DiceGroup(num_blue=10, num_green=3, num_red=4)

    :param groups: An iterable of DiceGroups from which the maximum is to be computed from
    :return: A dice group with the maximum number of dice of each colour
    """
    counts = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for group in groups:
        counts['red'] = max(counts['red'], group.num_red)
        counts['green'] = max(counts['green'], group.num_green)
        counts['blue'] = max(counts['blue'], group.num_blue)

    return DiceGroup(counts['blue'], counts['green'], counts['red'])


def parse_game_string(game_string: str) -> Iterable[DiceGroup]:
    """
    Returns a collection of DiceGroups from a game string.

    >>> [group for group in parse_game_string("Game 1: 1 green, 7 red; 1 green, 9 red, 3 blue")]
    [DiceGroup(num_blue=0, num_green=1, num_red=7), DiceGroup(num_blue=3, num_green=1, num_red=9)]

    :param game_string: A string representation of a game
    :return: An iterator of DiceGroups
    """

    for game in game_string.split(":")[1].strip().split(";"):
        counts = {
            "blue": 0,
            "green": 0,
            "red": 0
        }

        for collection in game.strip().split(','):
            for colour in counts:
                if colour in collection:
                    counts[colour] = int(collection.strip().split(' ')[0])
                    break

        yield DiceGroup(counts['blue'], counts['green'], counts['red'])


def validate_game(game: Iterable[DiceGroup], bag: DiceGroup) -> bool:
    """
    Validates a game given a bag.

    >>> bag = DiceGroup(14, 13, 12)
    >>> valid_game = [DiceGroup(3,0,4), DiceGroup(6,2,1), DiceGroup(0,2,0)]
    >>> validate_game(valid_game, bag)
    True

    >>> invalid_game = [DiceGroup(6,8,20), DiceGroup(5,13,4), DiceGroup(0,5,1)]
    >>> validate_game(invalid_game, bag)
    False

    :param game: A collection of DiceGroup that represent a game
    :param bag: A DiceGroup that represents the contents of a bag
    :return: A boolean representing whether a game is valid
    """

    for group in game:
        if group > bag:
            return False

    return True


def get_game_number(game_str: str) -> int:
    """
    Returns the game number give a game string.

    >>> get_game_number("Game 1: 1 green, 7 red; 1 green, 9 red, 3 blue")
    1
    >>> get_game_number("Game 100: 1 green, 7 red; 1 green, 9 red, 3 blue")
    100

    :param game_str: A string representation of a game
    """
    return int(game_str.split(':')[0].split(" ")[1])


def validate_games_file(path: Path, bag: DiceGroup) -> Iterable[Tuple[int, bool]]:
    for game_string in open(path):

        game_string = game_string.strip()

        groups = parse_game_string(game_string)
        game_number = get_game_number(game_string)
        valid_game = validate_game(groups, bag)

        yield game_number, valid_game


def total_power_games_file(path: Path) -> int:

    total_power = 0

    for game_string in open(path):

        game_string = game_string.strip()

        groups = parse_game_string(game_string)
        minimal_bag = max_dice_group(groups)

        total_power += minimal_bag.power()

    return total_power



if __name__ == "__main__":
    import doctest
    import argparse
    doctest.testmod()

    parser = argparse.ArgumentParser(prog='d2',
                    description="Decodes data from Advent of Code '23, Day 2")
    parser.add_argument('-i', '--infile', default='in/d2.txt', type=Path)
    parser.add_argument('-r', '--red', default=12, type=int)
    parser.add_argument('-b', '--blue', default=14, type=int)
    parser.add_argument('-g', '--green', default=13, type=int)
    #parser.add_argument('-w', '--wordcorrection', default=False, type=bool)

    args = parser.parse_args()

    valid_total = 0

    bag = DiceGroup(args.blue, args.green, args.red)

    for game_number, valid_game in validate_games_file(args.infile, bag=bag):
        valid_total += game_number if valid_game else 0

    power_total = total_power_games_file(args.infile)

    print(f"VALID TOTAL: {valid_total}")
    print(f"POWER TOTAL: {power_total}")
