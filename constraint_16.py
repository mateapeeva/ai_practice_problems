from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    for variable in variables:
        problem.addVariable(variable, Domain(set(range(10))))

    # ---Tuka dodadete gi ogranichuvanjata----------------

    # Constraint 0: all different
    problem.addConstraint(AllDifferentConstraint(),variables)

    # Constraint General:
    def constraint_general(*allvars):
        s,e,n,d,m,o,r,y = allvars
        if 1000*s + 100*e + 10*n + 1*d + 1000*m + 100*o + 10*r + 1*e == 10000*m + 1000*o + 100*n + 10*e + 1*y:
            return True

        return False


    problem.addConstraint(constraint_general,variables)


    # ----------------------------------------------------

    print(problem.getSolution())