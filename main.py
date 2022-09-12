import json

from input_parser import InputParser
from solver import Solver
from model import SudokuModel

FILEPATH = "puzzles/irregular.txt"
parser = InputParser(FILEPATH)
model = SudokuModel(parser.parse())
model.add_constraints()

# Useful for checking you have inputted the puzzle correctly
print(json.dumps(model.input, indent=2))

solver = Solver(model)
solution = solver.solve()
size = len(solution)

solution_string = ""
for i in range(size):
    for j in range(size):
        for k in range(size):
            if solution[i][j][k].x == 1:
                solution_string += str(k + 1)
                break

print("\n== SOLUTION ==\n")
for i in range(size):
    print(solution_string[i*size: (i+1)*size])
