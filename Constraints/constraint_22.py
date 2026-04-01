from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    lecture_slots_AI = input()
    lecture_slots_ML = input()
    lecture_slots_R = input()
    lecture_slots_BI = input()

    AI_lectures_domain = ["Mon_11", "Mon_12", "Wed_11", "Wed_12", "Fri_11", "Fri_12"]
    ML_lectures_domain = ["Mon_12", "Mon_13", "Mon_15", "Wed_12", "Wed_13", "Wed_15", "Fri_11", "Fri_12", "Fri_15"]
    R_lectures_domain = ["Mon_10", "Mon_11", "Mon_12", "Mon_13", "Mon_14", "Mon_15", "Wed_10", "Wed_11", "Wed_12",
                         "Wed_13", "Wed_14", "Wed_15", "Fri_10", "Fri_11", "Fri_12", "Fri_13", "Fri_14", "Fri_15"]
    BI_lectures_domain = ["Mon_10", "Mon_11", "Wed_10", "Wed_11", "Fri_10", "Fri_11"]

    AI_exercises_domain = ["Tue_10", "Tue_11", "Tue_12", "Tue_13", "Thu_10", "Thu_11", "Thu_12", "Thu_13"]
    ML_exercises_domain = ["Tue_11", "Tue_13", "Tue_14", "Thu_11", "Thu_13", "Thu_14"]
    BI_exercises_domain = ["Tue_10", "Tue_11", "Thu_10", "Thu_11"]

    # ---Add the variables here--------------------
    variables = []
    for i in range (1,int(lecture_slots_AI)+1):
        problem.addVariable("AI_lecture_"+str(i),AI_lectures_domain)
        variables.append("AI_lecture_"+str(i))
    for i in range (1,int(lecture_slots_ML)+1):
        problem.addVariable("ML_lecture_"+str(i),ML_lectures_domain)
        variables.append("ML_lecture_"+str(i))
    for i in range (1,int(lecture_slots_R)+1):
        problem.addVariable("R_lecture_"+str(i),R_lectures_domain)
        variables.append("R_lecture_"+str(i))
    for i in range (1,int(lecture_slots_BI)+1):
        problem.addVariable("BI_lecture_"+str(i),BI_lectures_domain)
        variables.append("BI_lecture_"+str(i))

    problem.addVariable("AI_exercises", AI_exercises_domain)
    variables.append("AI_exercises")

    problem.addVariable("ML_exercises", ML_exercises_domain)
    variables.append("ML_exercises")

    problem.addVariable("BI_exercises", BI_exercises_domain)
    variables.append("BI_exercises")


    # ---Add the constraints here----------------

    # Constraint 1: All different
    problem.addConstraint(AllDifferentConstraint(), variables)

    # Constraint 2: ML time lectures != time exercises
    for i in range (1,int(lecture_slots_ML)+1):
        problem.addConstraint(
            lambda lecture,exercises:
            False if lecture.split('_')[1] == exercises.split('_')[1] else True,
            ("ML_lecture_"+str(i),"ML_exercises"))

    # Constraint 3: 2h per lecture
    def constraint_general(*allvariables):
        for var1 in allvariables:
            for var2 in allvariables:
                if var2 < var1 and var1.split('_')[0] == var2.split('_')[0]:
                    if abs(int(var1.split('_')[1]) - int(var2.split('_')[1])) < 2:
                        return False

        return True
    problem.addConstraint(constraint_general,variables)

    # ----------------------------------------------------
    solution = problem.getSolution()

    print(solution)