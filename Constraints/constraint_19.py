from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    n = int(input())

    variables = list(range(1,n+1))
    domain = [(r,c) for r in range(n) for c in range(n)]

    problem.addVariables(variables,domain)

    problem.addConstraint(AllDifferentConstraint(),variables)

    def constraint_func(queen1,queen2):
        r_1,c_1 = queen1
        r_2,c_2 = queen2
        if abs(r_1-r_2) == abs(c_1-c_2):
            return False
        elif abs(r_1-r_2) == 0 or abs(c_1-c_2) == 0:
            return False

        return True

    for queen1 in variables:
        for queen2 in variables:
            if queen2 < queen1:
                problem.addConstraint(constraint_func,(queen1,queen2))

    if n < 7:
            solutions = problem.getSolutions()
            print(len(solutions))
    else:
            solutions = problem.getSolution()
            print(solutions)
