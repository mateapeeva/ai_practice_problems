from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    variables = ["Marija_attendance","Simona_attendance","Petar_attendance","time_meeting"]
    # Add the domains
    problem.addVariable("Marija_attendance", [0,1])
    problem.addVariable("Simona_attendance", [1])
    problem.addVariable("Petar_attendance", [0,1])
    problem.addVariable("time_meeting", [13,14,16,19])
    # ----------------------------------------------------

    # ---Add the constraints----------------

    # Constraint Marija
    def constraint(*all_vars):
        m,s,p,t = all_vars
        if m == 1 and t not in [14,15,18]:
            return False
        if p == 1 and t not in [12,13,16,17,18,19]:
            return False
        return True


    problem.addConstraint(constraint,variables)
    problem.addConstraint(MinSumConstraint(2),(variables[0],variables[1],variables[2]))
    # ----------------------------------------------------

    [print(solution) for solution in problem.getSolutions()]