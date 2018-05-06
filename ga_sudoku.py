import numpy
import random
import copy

dim = 9


def is_row_duplicate(board, row, value):
    return any(board[row][column] == value for column in range(dim))


def is_column_duplicate(board, column, value):
    return any(board[row][column] == value for row in range(dim))


def is_block_duplicate(board, row, column, value):
    i = 3 * (int(row / 3))
    j = 3 * (int(column / 3))
    block = [
        board[i][j], board[i][j + 1], board[i][j + 2], board[i + 1][j],
        board[i + 1][j + 1], board[i + 1][j + 2], board[i + 2][j],
        board[i + 2][j + 1], board[i + 2][j + 2]
    ]
    for pos in block:
        if pos == value:
            return True
    return False


class Population(object):

    def __init__(self):
        self.chromosomes = []
        return

    def seed(self, num_chromosomes, input_puzzle):
        self.chromosomes = []

        helper = Chromosome()
        helper.values = [[[] for j in range(0, dim)] for i in range(0, dim)]
        for row in range(0, dim):
            for column in range(0, dim):
                for value in range(1, 10):
                    if ((input_puzzle[row][column] == 0) and not (
                            is_column_duplicate(input_puzzle, column, value) or
                            is_block_duplicate(input_puzzle, row, column, value)
                            or is_row_duplicate(input_puzzle, row, value))):

                        helper.values[row][column].append(value)
                    elif (input_puzzle[row][column] != 0):

                        helper.values[row][column].append(
                            input_puzzle[row][column])
                        break

        for p in range(0, num_chromosomes):
            g = Chromosome()
            for i in range(0, dim):
                row = numpy.zeros(dim)

                for j in range(0, dim):

                    if (input_puzzle[i][j] != 0):
                        row[j] = input_puzzle[i][j]

                    elif (input_puzzle[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(
                            0,
                            len(helper.values[i][j]) - 1)]

                while (len(list(set(row))) != dim):
                    for j in range(0, dim):
                        if (input_puzzle[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(
                                0,
                                len(helper.values[i][j]) - 1)]

                g.values[i] = row

            self.chromosomes.append(g)

        self.update_fitness()
        print("Population seeding is complete.")

    def update_fitness(self):
        for chromosome in self.chromosomes:
            chromosome.update_fitness()

    def sort(self):
        self.chromosomes.sort(key=lambda a: a.fitness, reverse=True)


class Chromosome(object):

    def __init__(self):
        self.values = numpy.zeros((dim, dim))
        self.fitness = 0.0

    def update_fitness(self):
        column_count = numpy.zeros(dim)
        block_count = numpy.zeros(dim)
        column_sum = 0
        block_sum = 0

        for i in range(dim):
            for j in range(0, dim):
                column_count[int(self.values[i][j] - 1)] += 1

            column_sum += (1.0 / len(set(column_count))) / dim
            column_count = numpy.zeros(dim)

        for i in range(0, dim, 3):
            for j in range(0, dim, 3):
                block_count[int(self.values[i][j] - 1)] += 1
                block_count[int(self.values[i][j + 1] - 1)] += 1
                block_count[int(self.values[i][j + 2] - 1)] += 1

                block_count[int(self.values[i + 1][j] - 1)] += 1
                block_count[int(self.values[i + 1][j + 1] - 1)] += 1
                block_count[int(self.values[i + 1][j + 2] - 1)] += 1

                block_count[int(self.values[i + 2][j] - 1)] += 1
                block_count[int(self.values[i + 2][j + 1] - 1)] += 1
                block_count[int(self.values[i + 2][j + 2] - 1)] += 1

                block_sum += (1.0 / len(set(block_count))) / dim
                block_count = numpy.zeros(dim)

        if (int(column_sum) == 1 and int(block_sum) == 1):
            fitness = 1.0
        else:
            fitness = column_sum * block_sum

        self.fitness = fitness

    def mutate(self, mutation_rate, input_puzzle):
        r = random.uniform(0, 1.0)
        if (r < mutation_rate):
            while (True):
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1

                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while (from_column == to_column):
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)

                if (input_puzzle[row1][from_column] == 0 and
                        input_puzzle[row1][to_column] == 0):

                    if (not is_column_duplicate(input_puzzle, to_column,
                                                self.values[row1][from_column])
                            and not is_column_duplicate(
                                input_puzzle, from_column,
                                self.values[row2][to_column]) and
                            not is_block_duplicate(
                                input_puzzle, row2, to_column,
                                self.values[row1][from_column]) and
                            not is_block_duplicate(
                                input_puzzle, row1, from_column,
                                self.values[row2][to_column])):

                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][
                            from_column]
                        self.values[row1][from_column] = temp
                        break

    @staticmethod
    def crossover(parent1, parent2):
        child1 = Chromosome()
        child2 = Chromosome()

        child1.values = numpy.copy(parent1.values)
        child2.values = numpy.copy(parent2.values)

        crossover_point1 = random.randint(0, 8)
        crossover_point2 = random.randint(1, 9)
        while (crossover_point1 == crossover_point2):
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)

        if (crossover_point1 > crossover_point2):
            temp = crossover_point1
            crossover_point1 = crossover_point2
            crossover_point2 = temp

        for i in range(crossover_point1, crossover_point2):
            row1, row2 = child1.values[i], child2.values[i]
            child_row1 = numpy.zeros(dim)
            child_row2 = numpy.zeros(dim)

            remaining = list(range(1, dim + 1))
            cycle = 0

            while ((0 in child_row1) and (0 in child_row2)):
                if (cycle % 2 == 0):
                    index = next(
                        i for i in range(len(row1)) if row1[i] in remaining)
                    start = row1[index]
                    remaining.remove(row1[index])
                    child_row1[index] = row1[index]
                    child_row2[index] = row2[index]
                    next_pos = row2[index]

                    while (next_pos != start):
                        index = next(
                            i for i in range(len(row1)) if row1[i] == next_pos)
                        child_row1[index] = row1[index]
                        remaining.remove(row1[index])
                        child_row2[index] = row2[index]
                        next_pos = row2[index]

                    cycle += 1

                else:
                    index = next(
                        i for i in range(len(row1)) if row1[i] in remaining)
                    start = row1[index]
                    remaining.remove(row1[index])
                    child_row1[index] = row2[index]
                    child_row2[index] = row1[index]
                    next_pos = row2[index]

                    while (next_pos != start):
                        index = next(
                            i for i in range(len(row1)) if row1[i] == next_pos)
                        child_row1[index] = row2[index]
                        remaining.remove(row1[index])
                        child_row2[index] = row1[index]
                        next_pos = row2[index]

                    cycle += 1

            child1.values[i], child2.values[i] = child_row1, child_row2
        return child1, child2

    @staticmethod
    def selection_by_competition(chromosomes):
        candidates_copy = copy.deepcopy(chromosomes)
        random.shuffle(candidates_copy)
        ten_candidates = candidates_copy[:10]
        return max(ten_candidates, key=lambda a: a.fitness)


class Sudoku(object):

    def __init__(self, p):
        input_formatted = [x if x != '.' else '0' for x in p]
        self.input_puzzle = numpy.array(input_formatted).reshape((dim,dim)).astype(int)

    def save(self, path, solution):
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(dim * dim), fmt='%d')

    def solve_puzzle(self):
        print("==================")
        print("Genetic Algorithm")
        print("==================")
        num_chromosomes = 100
        num_elites = int(0.1 * num_chromosomes)
        num_generations = 1000
        mutation_rate = 0.1

        self.population = Population()
        self.population.seed(num_chromosomes, self.input_puzzle)

        stale_count = 0
        for generation in range(0, num_generations):

            #print("Generation %d" % generation)

            best_fitness = 0.0
            for c in range(0, num_chromosomes):
                fitness = self.population.chromosomes[c].fitness
                if (fitness == 1):
                    print("Solution found at generation %d!" % generation)
                    return self.population.chromosomes[c].values.astype(int)

                if (fitness > best_fitness):
                    best_fitness = fitness

            next_population = []

            self.population.sort()
            elites = []
            for e in range(0, num_elites):
                elite = Chromosome()
                elite.values = numpy.copy(self.population.chromosomes[e].values)
                elites.append(elite)

            for non_elite in range(num_elites, num_chromosomes, 2):
                parent1 = Chromosome.selection_by_competition(
                    self.population.chromosomes)
                parent2 = Chromosome.selection_by_competition(
                    self.population.chromosomes)

                child1, child2 = Chromosome.crossover(parent1, parent2)

                child1.mutate(mutation_rate, self.input_puzzle)
                child1.update_fitness()

                child2.mutate(mutation_rate, self.input_puzzle)
                child2.update_fitness()

                next_population.append(child1)
                next_population.append(child2)

            for e in range(0, num_elites):
                next_population.append(elites[e])

            self.population.chromosomes = next_population
            self.population.update_fitness()

            self.population.sort()
            if (self.population.chromosomes[0].fitness !=
                    self.population.chromosomes[1].fitness):
                stale_count = 0
            else:
                stale_count += 1

            if (stale_count >= 100):
                print("Stale poulation. Re-seeding...")
                self.population.seed(num_chromosomes, self.input_puzzle)
                stale_count = 0

        print("No solution found.")
        return None


if __name__ == "__main__":
    sudoku = Sudoku()
    solution = sudoku.solve_puzzle()
    #if solution: sudoku.save("ga_solution.txt", solution)
