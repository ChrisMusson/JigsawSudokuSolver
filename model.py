from mip import BINARY, Model, xsum


class SudokuModel(Model):

    def __init__(self, input: dict[str: list[str]]) -> None:
        super().__init__()
        self.input = input

        self.size = len(self.input["givens"])

        # define sol, the solution 3D boolean matrix where correct value is given
        # by the index (+1) where k == 1
        self.sol = [[[self.add_var(var_type=BINARY) for i in range(self.size)]
                     for j in range(self.size)] for k in range(self.size)]

    def add_standard_constraints(self):
        # exactly 1 value per cell
        for i in range(self.size):
            for j in range(self.size):
                self += xsum(self.sol[i][j][k] for k in range(self.size)) == 1

        # numbers 1-size in each row
        for i in range(self.size):
            for k in range(self.size):
                self += xsum(self.sol[i][j][k] for j in range(self.size)) == 1

        # numbers 1-size in each column
        for j in range(self.size):
            for k in range(self.size):
                self += xsum(self.sol[i][j][k] for i in range(self.size)) == 1

    def add_given_constraints(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                char = self.input["givens"][i][j]
                if char != ".":
                    self += self.sol[i][j][int(char) - 1] == 1

    def add_region_constraints(self):
        # numbers 1-size in each region
        regions = self.input["regions"]
        if not regions:
            return

        # for each letter in regions, get all cells that correspond to that letter
        region_cells = []
        region_names = sorted(set.union(*map(set, self.input["regions"])))
        for r in region_names:
            lst = []
            for i in range(self.size):
                for j in range(self.size):
                    if r == regions[i][j]:
                        lst.append((i + 1, j + 1))
            region_cells.append(lst)

        for cells in region_cells:
            for k in range(self.size):
                self += xsum(self.sol[cell[0] - 1][cell[1] - 1][k]
                             for cell in cells) == 1

    def add_constraints(self):
        self.add_standard_constraints()
        self.add_given_constraints()
        self.add_region_constraints()
