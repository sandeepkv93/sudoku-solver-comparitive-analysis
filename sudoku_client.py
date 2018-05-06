import sys
from sudokuGenerator import SudokuGenerator
import sudoku_test_case_generator
import SudokuSolver

'''
def dfsb_plus(puzzle):


def genetic(puzzle):
'''

def dancing_links(puzzle):
	sg = SudokuGenerator(puzzle)
	sg.generateBoard()
	sudoku_solver = SudokuSolver.SudokuSolver(sg.getGrid())
	sudoku_solver.generateLinks()
	sudoku_solver = sudoku_solver.solve()

def solve_sudoku(puzzle):
	#dfsb_plus(puzzle)
	#genetic(puzzle)
	dancing_links(puzzle)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Invalid Input!')
		print('python sudoku_client.py <level>')
		print('1: easy; 2: medium; 3: difficult')
	
	level = sys.argv[1]
	puzzle = sudoku_test_case_generator.generateSudokuInput(level)
	solve_sudoku(puzzle)