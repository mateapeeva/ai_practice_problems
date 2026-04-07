from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ----------------------------------------------------
    # ---Prochitajte gi informaciite od vlezot
    num_trees = int(input())
    trees_pos = [tuple(map(int, input().split())) for _ in range(num_trees)]
    number_per_col = list(map(int, input().split()))

    variables = [f"Tree{i}" for i in range(num_trees)]
    full_domains = [(x,y) for x in range(6) for y in range(6)]
    domains = [pos for pos in full_domains if pos not in trees_pos]

    # -----------------------------------------------------
    # ---Izberete promenlivi i domeni so koi bi sakale da rabotite-----

    problem.addVariables(variables, domains)

    # -----------------------------------------------------
    # ---Potoa dodadete ogranichuvanjata-------------------

    # Constraint 1: All different tree
    problem.addConstraint(AllDifferentConstraint(),variables)

    # Constraint 2: It can not be on tree position
    for tree in trees_pos:
        problem.addConstraint(lambda *v, t=tree: tree not in v, variables)

    # # Constraint 3: Can not be neighbors
    #
    # def constraint3(v1,v2):
    #     x1,y1 = v1
    #     x2,y2 = v2
    #     if max(abs(x1-x2),abs(y1-y2)) == 1:
    #         return False
    #     return True
    #
    #
    # for tree1 in variables:
    #     for tree2 in variables:
    #         if tree1 != tree2:
    #             problem.addConstraint(constraint3,(tree1,tree2))

    # Constraint 4: Has to be next to tree
    def is_next_tree(tent,tree):
        dist = abs(tent[0]-tree[0])+abs(tent[1]-tree[1])
        return dist == 1

    for i in range(num_trees):
        tent = variables[i]
        tree = trees_pos[i]
        problem.addConstraint(lambda te,tr=tree:is_next_tree(te,tr),[tent])

    # Constraint 5: Col sum:
    def col_sum(*vars,cols):
        count = [0 for _ in range(6)]
        cols = list(cols)
        for var in vars:
            x = var[0]
            count[x] += 1
        return count == cols
    problem.addConstraint(lambda *vars, c=tuple(number_per_col): col_sum(*vars,cols=c), variables)

    # -----------------------------------------------------
    # ---Potoa pobarajte reshenie--------------------------

    solution = problem.getSolution()

    # -----------------------------------------------------
    # ---Na kraj otpechatete gi poziciite na shatorite-----
    if solution:
        for i in range(num_trees):
            print(f"{solution[f'Tree{i}'][0]} {solution[f'Tree{i}'][1]}")


