import numpy as np

BOARDER = '-------------------------\n'

# This class contains all the details needed for validating a Sudoku
class SudokuValidator(object):

	def __init__(self,line=None,grid=[]):
		self.line = line
		self.grid = grid

	def generateBoard(self):
		grid = []
		for c in self.line:
			if c == '.':
				grid.append(0)
			else:
				grid.append(int(c))
		self.grid = np.array(grid).reshape(9,9)

	# Makes sure the contraints are satisfied in rows,columns and boxes.
	def checkrowcol(self, row, col):
		currentRow = []
		for cell in self.grid[row]:
			if cell != 0 and (cell not in currentRow):
				currentRow.append(cell)
			elif cell != 0:
				return 1
		for cell in self.grid[row]:
			if cell == 0:
				return 0

		transposeMatrix = np.transpose(self.grid)
		currentCol = []
		for cell in self.grid[col]:
			if cell != 0 and (cell not in currentCol):
				currentCol.append(cell)
			elif cell != 0:
				return 1
		for cell in self.grid[col]:
			if cell == 0:
				return 0

		# This stores the range of rows and columns that needs to be considered 
		# for validating boxes.
		BoxStartEndRange = {
			'0': [(0, 3), (0, 3)], '1': [(0, 3), (3, 6)], '2': [(0, 3), (6, 9)],
			'3': [(3, 6), (0, 3)], '4': [(3, 6), (3, 6)], '5': [(3, 6), (6, 9)],
			'6': [(6, 9), (0, 3)], '7': [(6, 9), (3, 6)], '8': [(6, 9), (6, 9)]
		}

		solutionFound = True
		correctk = 0
		for k in range(0, 9):
			for i in range(BoxStartEndRange[str(k)][0][0], BoxStartEndRange[str(k)][0][1]):
				for j in range(BoxStartEndRange[str(k)][1][0], BoxStartEndRange[str(k)][1][1]):
					if(row == i or col == j):
						correctk = k
						break

		currentBox = []
		for i in range(BoxStartEndRange[str(correctk)][0][0], BoxStartEndRange[str(correctk)][0][1]):
			for j in range(BoxStartEndRange[str(correctk)][1][0], BoxStartEndRange[str(correctk)][1][1]):
				if self.grid[i][j] != 0 and (self.grid[i][j] not in currentBox):
					currentBox.append(self.grid[i][j])
				elif self.grid[i][j] != 0:
					return 1

		for i in range(BoxStartEndRange[str(correctk)][0][0], BoxStartEndRange[str(correctk)][0][1]):
			for j in range(BoxStartEndRange[str(correctk)][1][0], BoxStartEndRange[str(correctk)][1][1]):
				if self.grid[i][j] == 0:
					return 0
		return 1

	# This function checks for validation as well and it is used by DFS for 
	# checking the validation.
	def checkBoard(self):
		numberOfRows = self.grid.shape[0]
		numberOfColumns = self.grid.shape[1]

		for row in range(0, numberOfRows):
			currentRow = []
			for cell in self.grid[row]:
				if cell != 0 and (cell not in currentRow):
					currentRow.append(cell)
				elif cell != 0:
					return 1
			for cell in self.grid[row]:
				if cell == 0:
					return 0

		transposeMatrix = np.transpose(self.grid)
		for col in range(0,numberOfColumns):
			currentColumn = []
			for cell in transposeMatrix[col]:
				if cell != 0 and (cell not in currentColumn):
					currentColumn.append(cell)
				elif cell != 0:
					return 1
			for cell in transposeMatrix[col]:
				if cell == 0:
					return 0

		BoxStartEndRange = {
							'0': [(0,3),(0,3)], '1': [(0,3),(3,6)], '2': [(0,3),(6,9)],
							'3': [(3,6),(0,3)], '4': [(3,6),(3,6)], '5': [(3,6),(6,9)],
							'6': [(6,9),(0,3)],  '7': [(6,9),(3,6)], '8': [(6,9),(6,9)]
							}

		solutionFound = True
		for k in range(0,9):
			currentBox = []
			for i in range(BoxStartEndRange[str(k)][0][0],BoxStartEndRange[str(k)][0][1]):
				for j in range(BoxStartEndRange[str(k)][1][0],BoxStartEndRange[str(k)][1][1]):
					if self.grid[i][j] != 0 and (self.grid[i][j] not in currentBox):
						currentBox.append(self.grid[i][j])
					elif self.grid != 0:
						return 1
			for i in range(BoxStartEndRange[str(k)][0][0], BoxStartEndRange[str(k)][0][1]):
				for j in range(BoxStartEndRange[str(k)][1][0], BoxStartEndRange[str(k)][1][1]):
					if self.grid[i][j] == 0:
						return 0
		return 2

	# This validation is performed after every solution that is generated to 
	# check if the contraints are satisfied.
	def validateBoard(self, solutionFound=False):
		numberOfRows = self.grid.shape[0]
		numberOfColumns = self.grid.shape[1]

		for row in range(0, numberOfRows):
			currentRow = []
			for cell in self.grid[row]:
				if solutionFound and (cell not in currentRow) and (cell > 0 and cell < 9):
					currentRow.append(cell)
					continue
				elif not solutionFound and (cell < 0 or cell > 9):
					print("Error in given data")
					return False
				elif solutionFound:
					print("Error in solution found")
					return False

		transposeMatrix = np.transpose(self.grid)
		for col in range(0,numberOfColumns):
			currentColumn = []
			for cell in transposeMatrix[col]:
				if solutionFound and (cell not in currentColumn) and (cell > 0 and cell < 9):
					currentColumn.append(cell)
					continue
				elif not solutionFound and (cell < 0 or cell > 9):
					print("Error in given data")
					return False
				elif solutionFound:
					print("Error in solution found")
					return False

		BoxStartEndRange = {
							'0': [(0,3),(0,3)], '1': [(0,3),(3,6)], '2': [(0,3),(6,9)],
							'3': [(3,6),(0,3)], '4': [(3,6),(3,6)], '5': [(3,6),(6,9)],
							'6': [(6,9),(0,3)],  '7': [(6,9),(3,6)], '8': [(6,9),(6,9)]
							}

		for k in range(0,9):
			currentBox = []
			for i in range(BoxStartEndRange[str(k)][0][0],BoxStartEndRange[str(k)][0][1]):
				for j in range(BoxStartEndRange[str(k)][1][0],BoxStartEndRange[str(k)][1][1]):
					if solutionFound and (self.grid[i][j] > 0 and self.grid[i][j] < 9) and (self.grid[i][j] not in currentBox):
						currentBox.append(self.grid[i][j])
						continue
					elif not solutionFound and (cell < 0 or cell > 9):
						print("Error in given data")
						return False
					elif solutionFound:
						print("Error in solution found")
						return False
		return True

	# This function prints the board in Sudoku board format.
	def printBoard(self):
		board = BOARDER
		for i, row in enumerate(self.grid):
			num = str(row)[1:-1]
			board += "| %s | %s | %s | \n" % ( num[0:5], num[6:11], num[12:17])
			if (i+1) % 3 == 0:
				board += BOARDER
		return board

	def getGrid(self):
		return self.grid

