import numpy as np

from sudokuGenerator import SudokuGenerator

class DataObject(object):

	def __init__(self,C,ID):
		self.R = self
		self.L = self
		self.U = self
		self.D = self
		self.C = C
		self.ID = ID

class ColumnObject(object):

	def __init__(self,ide):
		#self.dataObject = DataObject(self,ide)
		DataObject.__init__(self,self,ide)
		self.count = 0

class SudokuSolver(object):

	def __init__(self, grid):
		self.solution = []
		self.grid = grid
		self.h = None

	def LinkRowToColumn(self,rowElement):
		top = rowElement.C 
		rowElement.C.count +=1
		rowElement.D = top
		rowElement.U = top.U 
		top.U.D = rowElement
		top.U = rowElement

	def createRows(self,i,j,k,columnList):
		rowNumber = i*81 + j*9 + k
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

	def chooseColumn(self):
		c = self.h.R
		currentCount = 1000
		while c != self.h:
			if c.count < currentCount:
				selectedColumn = c
				currentCount = c.count
			c = c.R
		return selectedColumn

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

	def search(self,resultFound):
		if resultFound:
			return

		if self.h == self.h.R:
			resultFound = True
			print("Solution Found")
			grid = self.buildSolution()
			res = SudokuGenerator(None,grid)
			if res.validateBoard():
				print(res.printBoard())
			else:
				print("Result Found is not valid")
				resultFound = False
			return
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
		if self.h != self.h.R:
			return self.search(False)


	def buildSolution(self):
		rows = []
		for r in self.solution:
			rows.append(r.ID)
		rows.sort()
		grid = []
		for n in rows:
			grid.append(n % 9 + 1)

		return np.array(grid).reshape(9,9)

print("In main")
s = SudokuGenerator(".......12........3..23..4....18....5.6..7.8.......9.....85.....9...4.5..47...6...")
s.generateBoard()
print(s.validateBoard())
print(s.printBoard())
x = s.getGrid()
s1 = SudokuSolver(x)
s1.generateLinks()
sol = s1.solve()
