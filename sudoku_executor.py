import sys
import sudokuValidator
import sudoku_test_case_generator
import sudoku_csp
import DancingLinks
import ga_sudoku
import time

execution_time = {}


def dfsb_plus(puzzle):
    s = sudokuValidator.SudokuValidator(puzzle)
    s.generateBoard()
    print(s.printBoard())
    start = time.time()
    s = sudoku_csp.solveSudoku_DFS_AC3(s)
    end = time.time()
    execution_time['dfsb_ac3'] = (end - start) * 1000
    print(s.printBoard())


def genetic(puzzle):
    sga = ga_sudoku.Sudoku(puzzle)
    start = time.time()
    solution = sga.solve_puzzle()
    end = time.time()
    execution_time['genetic'] = (end - start) * 1000
    if solution is not None:
        print(sudokuValidator.printBoard(solution))


def dancing_links(puzzle):
    sg = sudokuValidator.SudokuValidator(puzzle)
    sg.generateBoard()
    start = time.time()
    sudoku_solver = DancingLinks.SudokuSolver(sg.getGrid())
    sudoku_solver.generateLinks()
    sudoku_solver = sudoku_solver.solve()
    end = time.time()
    execution_time['dancing_links'] = (end - start) * 1000


def solve_sudoku(puzzle):
    dfsb_plus(puzzle)
    genetic(puzzle)
    dancing_links(puzzle)
    print('\n=====================================')
    print('|             Analysis              |')
    print('=====================================\n')
    print("{:<15} {:<10}".format('Algorithm', 'Time Taken'))
    print('-------------------------------------')
    for k, v in execution_time.items():
        print("{:<15} {:<10}".format(k, v), 'ms')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Invalid Input!')
        print('python sudoku_client.py <level>')
        print('1: easy; 2: medium; 3: difficult')
        exit()

    level = int(sys.argv[1])
    puzzle = sudoku_test_case_generator.generateSudokuInput(level)
    solve_sudoku(puzzle)
