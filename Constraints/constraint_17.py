from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["A", "B", "C", "D", "E", "F"]

    for variable in variables:
        problem.addVariable(variable, Domain(set(range(100))))

    # ---Tuka dodadete gi ogranichuvanjata----------------

    # Constraint All Different
    problem.addConstraint(AllDifferentConstraint(),variables)

    # Constraint 1: B,D,E % 2 == 1
    problem.addConstraint(
        lambda b: True if b%2==1 else False,
        "B"
    )
    problem.addConstraint(
        lambda d: True if d % 2 == 1 else False,
        "D"
    )
    problem.addConstraint(
        lambda e: True if e % 2 == 1 else False,
        "E"
    )

    # Constraint 2: A+B+C >= 100
    problem.addConstraint(MinSumConstraint(100),("A","B","C"))


    # Constraint 3: D+E == 150
    problem.addConstraint(ExactSumConstraint(150),("D","E"))


    # Constraint 4: F%4 == 0
    problem.addConstraint(
        lambda f: True if (f%10) in [0,4,8] else False,
        ("F",)
    )

    # ----------------------------------------------------

    print(problem.getSolution())