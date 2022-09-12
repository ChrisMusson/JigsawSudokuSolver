from ast import parse
import re


class InputParser:

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read_file(self) -> list[str]:
        with open(self.filename, "r") as f:
            # strip whitespace from lines and remove any line that is only whitespace
            return list(filter(None, [x.strip().lower() for x in f.readlines()]))

    def parse_givens(self, input: list[str]) -> list[str]:
        pattern = re.compile("^[\d\.]{4,}$")
        return list(filter(pattern.match, input))

    def parse_regions(self, input: list[str]) -> list[str]:
        pattern = re.compile("^[a-z]{4,}$")
        return list(filter(pattern.match, input))

    def is_deficit(self, input: list[str]) -> bool:
        pattern = re.compile("^deficit:?.*true$")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_surplus(self, input: list[str]) -> bool:
        pattern = re.compile("^surplus:?.*true$")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def parse(self) -> dict[str, list[str] | bool]:
        parsed_puzzle = {}
        input = self.read_file()

        parsed_puzzle["givens"] = self.parse_givens(input)
        parsed_puzzle["regions"] = self.parse_regions(input)

        parsed_puzzle["deficit"] = self.is_deficit(input)
        parsed_puzzle["surplus"] = self.is_surplus(input)

        return parsed_puzzle
