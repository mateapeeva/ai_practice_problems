from constraint import *

if __name__ == '__main__':
    solver_in = input()
    problem = Problem(globals()[solver_in]())

    variables = list(range(81))
    domain = list(range(1,10))

    problem.addVariables(variables,domain)

    # Constraint 1: same block
    for row_start in range(0,9,3):
        for col_start in range(0,9,3):
            block_variables = []
            for i in range(3):
                for j in range(3):
                    block_variables.append((row_start+i)*9 + col_start+j)
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
        print(dict(sorted(solution.items())))
    else:
        print(None)