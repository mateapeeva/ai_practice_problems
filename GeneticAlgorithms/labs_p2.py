import pygad


N = int(input())
#S, E = map(int,input().split())

# With modification
E = int(input())

dist = [list(map(float, input().split())) for _ in range(N)]


# It needs to give us the two routes
def decode(solution):
    friend1_cities = []
    friend2_cities = []

    S = int(abs(solution[N])) % N
    if S == E:
        S = (S + 1) % N

    for city_index, val in enumerate(solution):
        if city_index == S or city_index == E or city_index == N:
            continue

        if val > 0:
            friend1_cities.append((val,city_index))
        else:
            friend2_cities.append((val,city_index))

    friend1_cities.sort(key=lambda x:x[0])
    friend2_cities.sort(key=lambda x:x[0], reverse=True)

    r1 = [city for _, city in friend1_cities]
    r2 = [city for _,city in friend2_cities]

    route1 = [S] + r1 + [E]
    route2 = [S] + r2 + [E]

    return route1,route2

# Minimize time, large penalty if time_friend1 = 2*time_friend2 or vice verse, if number of cities is not balanced small penalty
def fitness_func(ga, solution, idx):
    route1, route2 = decode(solution)

    balance_number_cities_penalty = 0
    time_difference_penalty = 0

    time_friend1 = 0
    for i in range(len(route1) - 1):
        time_friend1 += dist[route1[i]][route1[i+1]]

    time_friend2 = 0
    for i in range(len(route2) - 1):
        time_friend2 += dist[route2[i]][route2[i + 1]]

    max_time = max(time_friend1,time_friend2)
    min_time = min(time_friend1,time_friend2)

    if max_time >= 2*min_time:
        time_difference_penalty += 1000000

    max_cities = max(len(route1),len(route2))
    min_cities = min(len(route1),len(route2))

    if max_cities != min_cities:
        balance_number_cities_penalty += (max_cities-min_cities)*10000

    penalty = time_difference_penalty + balance_number_cities_penalty + max_time

    # You can return just -penalty, but apparently this is better and faster for pygad
    return 1.0 / penalty


# Sign tells us which friend: + -> 1, - -> 2
# When we sort them it tells us in which order are they visited
# N+1 is for starting city S
gene_space = [{'low':-N,'high':N}] * (N+1)


params = {
    'num_generations': 500,
    'sol_per_pop': 100,
    'num_parents_mating': 50,

    'num_genes': N+1,
    'gene_space': gene_space,

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'save_best_solutions': True,
}


ga = pygad.GA(**params)

ga.run()

solution, _, _ = ga.best_solution()
fitness = fitness_func(None, solution, 0)
best_solutions = ga.best_solutions

route1, route2 = decode(solution)

print("Friend 1 route:", route1)
print("Friend 2 route:", route2)
print("Fitness:", fitness)

# submit_data(fitness_func, decode, best_solutions)