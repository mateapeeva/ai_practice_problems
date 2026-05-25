import pygad
import random
random.seed(0)


# BIG ROOMS: 2, 8, 9, 10
# SMALL ROOMS: 1, 3, 4, 5, 6, 7


big_rooms = [2,8,9,10]

rooms = {
    1: {'name': 'Modern & Contemporary Art', 'adjacent': [2, 7], 'value': 110},
    2: {'name': 'European History', 'adjacent': [1, 3, 4, 5, 7], 'value': 130},
    3: {'name': 'Seasonal Exhibitions', 'adjacent': [2], 'value': 100},
    4: {'name': 'Prehistory', 'adjacent': [2, 6, 10], 'value': 140},
    5: {'name': 'Medieval Times', 'adjacent': [2, 6, 9], 'value': 120},
    6: {'name': 'Arms and Armor', 'adjacent': [4, 5], 'value': 150},
    7: {'name': 'Arts of Africa, Oceania and the Americas', 'adjacent': [1, 2, 8], 'value': 90},
    8: {'name': 'Greek and Roman History', 'adjacent': [7, 9], 'value': 180},
    9: {'name': 'The Great Hall', 'adjacent': [5, 8, 10], 'value': 30},
    10: {'name': 'Egyptian History', 'adjacent': [4, 9], 'value': 200}
}

# k cams
K = int(input())

# 100% coverage - 1 cam for small room, more than one not useful
# 60% - 1 cam, 100% - 2 cams for big room, more than two not useful
# +10% for adjacent rooms
# max 100%
# protected values = coverage% * value of room
def decode(solution):
    cams = [int(i) for i in solution]
    return cams

def fitness_func(ga, solution, idx):
    cams = decode(solution)
    num_cams = [0 for _ in range(11)]
    value = 0

    for cam in cams:
        num_cams[cam] += 1

    percent_per_room = [0 for _ in range(11)]
    for i,c in enumerate(num_cams):
        if i == 0:
            continue
        elif i not in big_rooms and c>=1:
            percent_per_room[i] += 100
        elif i in big_rooms and c >= 2:
            percent_per_room[i] += 100
        elif i in big_rooms and c == 1:
            percent_per_room[i] += 60


        if c >= 1:
            for room_adj in rooms[i]['adjacent']:
                percent_per_room[room_adj] += 10*c

    for i,percent in enumerate(percent_per_room):
        if i == 0:
            continue
        percent_per_room[i] = min(100,percent)
        value += percent_per_room[i] * rooms[i]['value'] / 100.0


    return value


gene_space = [{'low':1, 'high':11}]*K

params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    'num_genes': K,
    'gene_space': gene_space,

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'random_seed': 0
}

ga = pygad.GA(**params)

ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(None, best_solution, 0)

print(f'Optimal protected value: {best_fitness}M$')
print(f"{decode(best_solution)}")
