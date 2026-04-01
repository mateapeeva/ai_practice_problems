from constraint import *

if __name__ == '__main__':
    solvers = {
        "BacktrackingSolver": BacktrackingSolver(),
        "MinConflictsSolver": MinConflictsSolver(),
        "RecursiveBacktrackingSolver": RecursiveBacktrackingSolver()
    }

    solve = input()
    problem = Problem(solvers.get(solve))

    variables = list(range(81))
    domain = list(range(1,10))

    for var in variables:
        problem.addVariable(var,domain)

    # Constraint 1: same block
    for row_start in range(0,9,3):
        for col_start in range(0,9,3):
            block_variables = []
            for r in range(3):
                for c in range(3):
                    block_variables.append((row_start+r)*9 + col_start+c)
            problem.addConstraint(AllDifferentConstraint(),block_variables)

    # Constraint 2: row
    for row in range(9):
        row_variables = [row * 9 + col for col in range(9)]
        problem.addConstraint(AllDifferentConstraint(), row_variables)

    # Constraint 3: col
    for col in range(9):
        col_variables = [col + 9 * row for row in range(9)]
        problem.addConstraint(AllDifferentConstraint(), col_variables)

    solution = problem.getSolution()
    if solution is not None:
        print(solution)
    else:
        print(None)