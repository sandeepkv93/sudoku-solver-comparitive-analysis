import numpy as np
import time 
import sys 
from sudokuValidator import SudokuValidator

steps = 0
# The DataObject class defines all the information needed for every element in the sparse matrix.
class DataObject(object):

	def __init__(self,C,ID):
		self.R = self
		self.L = self
		self.U = self
		self.D = self
		self.C = C
		self.ID = ID

# This stores the information about the different columns(Different Constraints).
class ColumnObject(object):

	def __init__(self,ide):
		DataObject.__init__(self,self,ide)
		self.count = 0

# This is the main function where DLX algorithm is implemented. 
class SudokuSolver(object):

	def __init__(self, grid):
		self.solution = []
		self.grid = grid
		self.h = None

	# This function makes sure the elements of the row are linked to column and 
	# it increments the count of the column header.
	def LinkRowToColumn(self,rowElement):
		top = rowElement.C 
		rowElement.C.count +=1
		rowElement.D = top
		rowElement.U = top.U 
		top.U.D = rowElement
		top.U = rowElement

	# This function makes sure the different rows are created and then it calls 
	# the LinkRowToColumn to link it to the columns.
	def createRows(self,i,j,k,columnList):
		rowNumber = i*81 + j*9 + k

		# The calculation is as follows because of the constraint order we have used.
		# 1. Row Constraint
		# 2. Column Constraint
		# 3. Box Constraint
		# In total there are 324 contraints

		pos = DataObject(columnList[i*9 + j],rowNumber)
		row = DataObject(columnList[81 + i*9 + k],rowNumber)
		col = DataObject(columnList[162 + j*9 + k],rowNumber)
		box = DataObject(columnList[243 + (3*(i//3) + (j//3))*9 + k],rowNumber)
		
		pos.R = row 
		row.R = col
		col.R = box
		box.R = pos
		pos.L = box
		box.L = col
		col.L = row
		row.L = pos

		self.LinkRowToColumn(pos)
		self.LinkRowToColumn(row)
		self.LinkRowToColumn(col)
		self.LinkRowToColumn(box)

	# The generate links makes sure we generate different possible combinations 
	# of rows and assosicate it with appropriate columns. We generate different 
	# combinations only for empty spaces in the suodku.
	def generateLinks(self):

		h = ColumnObject('h')
		self.h = h
		columnList = list()

		for column in range(0,324):
			c = ColumnObject(column)
			c.R = h
			c.L = h.L
			h.L.R = c
			h.L = c
			columnList.append(c)

		for i in range(self.grid.shape[0]):
			for j in range(self.grid.shape[1]):
				if self.grid[i][j] == 0:
					for k in range(0,9):
						self.createRows(i,j,k,columnList)
				else:
					self.createRows(i,j,self.grid[i][j] - 1,columnList)

	# This will choose the column with the least number of elements in it.
	def chooseColumn(self):
		c = self.h.R
		currentCount = 1000
		while c != self.h:
			if c.count < currentCount:
				selectedColumn = c
				currentCount = c.count
			c = c.R
		return selectedColumn

	# This unlinks the element from the appropriate row and column. 
	def cover(self,column):
		column.L.R = column.R
		column.R.L = column.L

		row = column.D

		while row != column:
			j = row.R
			while j != row:
				j.U.D = j.D
				j.D.U = j.U
				j.C.count -= 1 
				j = j.R
			row = row.D

	# This links the element to the aprropriate row and column.
	def uncover(self,column):
		row = column.U
		while row != column:
			j = row.L 
			while j != row:
				j.D.U = j
				j.U.D = j
				j.C.count += 1
				j = j.L
			row = row.U

		column.R.L = column
		column.L.R = column

	# We call this function to perform the search for the solution. 
	# At each iteration it checks if there are any columns left and if the solution is satisfied.
	# We pick a column with least rows first and we move ahead by covering this 
	# column and all the columns where this row as a element in.
	# In the next iteration we pick the next column with the least number of rows.
	# If the solution is not found then we backtrack by calling uncover function.
	def search(self,resultFound):
		global steps

		steps = steps + 1

		if resultFound:
			return

		if self.h == self.h.R:
			resultFound = True
			grid = self.buildSolution()
			res = SudokuValidator(None,grid)
			if res.validateBoard():
				print(res.printBoard())
				print("steps:",steps)
			else:
				print("Result Found is not valid")
				resultFound = False
			exit()
		else:
			c = self.chooseColumn()
			self.cover(c)
			r = c.D
			while r != c:
				self.solution.append(r)
				currentRightElement = r.R
				while currentRightElement != r:
					self.cover(currentRightElement.C)
					currentRightElement = currentRightElement.R
				self.search(resultFound)

				r = self.solution.pop()
				c = r.C
				currentLeftElement = r.L
				while currentLeftElement != r:
					self.uncover(currentLeftElement.C)
					currentLeftElement = currentLeftElement.L
				r = r.D
			self.uncover(c)
			return 

	def solve(self):
		print('=======================')
		print('Dancing Link Algorithm')
		print('=======================')
		if self.h != self.h.R:
			return self.search(False)

	# This function retrieves the solution from the sparse matrix.
	def buildSolution(self):
		rows = []
		for r in self.solution:
			rows.append(r.ID)
		rows.sort()
		grid = []
		for n in rows:
			grid.append(n % 9 + 1)

		return np.array(grid).reshape(9,9)

