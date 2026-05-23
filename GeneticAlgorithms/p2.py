import pygad
import numpy as np


def compute_time(teams, preferred_category):
    total_time = 0

    for team in teams:
        times = [machines_info[m][0] for m in team]
        categories = [machines_info[m][1] for m in team]

        if all(c == preferred_category for c in categories):
            total_time += min(times)
        else:
            total_time += max(times)

    return total_time

def decode(solution):
    teams = []

    for i in range(0,len(solution),4):
        teams.append([int(x) for x in solution[i:i+4]])

    return teams

def fitness_func(ga_instance, solution, solution_idx):
    teams = decode(solution)

    all_categories = set(machines_info[m][1] for m in range(N))
    best_time, best_p_cat = min(
        (compute_time(teams,p),p) for p in all_categories
    )

    return 1.0 / best_time


if __name__ == '__main__':
    N = int(input())
    machines_info = []
    for _ in range(N):
        information = input().split()

        time = int(information[0])
        category = information[1]

        machines_info.append((time,category))

    num_teams = N // 4

    gene_space = list(range(N))

    params = {
        'num_generations': 300,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,
        'gene_space': gene_space,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,

        # ADDED BY ME
        'gene_type': int,
        'allow_duplicate_genes':False,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    teams = decode(best_solution)

    all_categories = set(machines_info[m][1] for m in range(N))
    best_time, best_p_cat = min(
        (compute_time(teams, p), p) for p in all_categories
    )

    #PRINT
    print("TEAMS:")
    for team in teams:
        print(team)

    print(f"Total time: {best_time}")
    print(f"Best preferred category: {best_p_cat}")