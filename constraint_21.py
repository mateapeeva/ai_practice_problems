from constraint import *

if __name__ == '__main__':
    num = int(input())

    papers = dict()

    paper_info = input()
    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        paper_info = input()


    # Define the variables
    variables = [paper for paper in papers.keys()]

    domain = [f'T{i + 1}' for i in range(num)]

    problem = Problem(BacktrackingSolver())

    # Change this section if necessary
    problem.addVariables(variables, domain)

    # Add the constraints

    # Constraint 1: max 4 papers per time-slot
    def constraint_1(*all_variables):
        count = [0 for _ in range(5)]
        for var in all_variables:
            index = int(var[len(var) - 1])
            count[index] += 1

        for i in range(5):
            if count[i] > 4:
                return False
        return True

    problem.addConstraint(constraint_1,variables)

    # Constraint 2: Category <= 4 -> same time-slot
    category_number = {"AI":0,"ML":0,"NLP":0}
    for paper in papers.keys():
        category_number[papers[paper]] += 1

    for category in category_number.keys():
        if category_number[category] in range(1,5):
            problem.addConstraint(AllEqualConstraint(),[paper for paper in papers.keys() if papers[paper] == category])


    result = problem.getSolution()

    # Add the required print section
    res = sorted(result.keys(),key=lambda x: int(x[5:]))
    for paper in result.keys():
        print(paper + " (" + papers[paper] + "): " + result[paper])
