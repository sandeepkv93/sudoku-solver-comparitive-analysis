import sys
from sudokuValidator import SudokuValidator
import sudoku_test_case_generator
import sudoku_csp
import DancingLinks

def dfsb_plus(puzzle):
	s = SudokuValidator(puzzle)
	s.generateBoard()
	print(s.printBoard())
	s = sudoku_csp.solveSudoku_DFS_AC3(s)
	print(s.printBoard())

'''
def genetic(puzzle):
'''

def dancing_links(puzzle):
	sg = SudokuValidator(puzzle)
	sg.generateBoard()
	sudoku_solver = DancingLinks.SudokuSolver(sg.getGrid())
	sudoku_solver.generateLinks()
	sudoku_solver = sudoku_solver.solve()
	return 

def solve_sudoku(puzzle):
	dfsb_plus(puzzle)
	#genetic(puzzle)
	dancing_links(puzzle)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Invalid Input!')
		print('python sudoku_client.py <level>')
		print('1: easy; 2: medium; 3: difficult')
	
	level = int(sys.argv[1])
	puzzle = sudoku_test_case_generator.generateSudokuInput(level)
	solve_sudoku(puzzle)