import pygad

N, M, R = map(float, input().split())
N = int(N)
M = int(M)

points = [tuple(map(float, input().split())) for _ in range(N)]

# Part 1.
def decode(solution):
    decode_sol = []
    for i in range(0,len(solution),2):
        pair = (solution[i],solution[i+1])
        decode_sol.append(pair)

    return decode_sol


def fitness_func(ga, solution, idx):
    centers = decode(solution)

    uncovered_penalty = 0
    overlap_penalty = 0
    umbrella_usage_penalty = 0
    more_points_covered = 0


    for px,py in points:
        covered = False
        for cx,cy in centers:
            dist = ((px-cx)**2 + (py-cy)**2) ** 0.5
            if dist <= R:
                covered = True
                break
        if not covered:
            uncovered_penalty += 1000000

    num_of_used_umbrellas = 0

    for cx,cy in centers[:-1]:
        num_of_points_covered = 0
        for px,py in points:
            dist = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
            if dist <= R:
                num_of_points_covered+=1

        if num_of_points_covered >= 1:
            num_of_used_umbrellas += 1
        if num_of_points_covered >= 2:
            more_points_covered += 50000

    num_umbrellas = len(centers)
    for i in range(num_umbrellas):
        for j in range(i+1,num_umbrellas):
            c1_x, c1_y = centers[i]
            c2_x, c2_y = centers[j]

            dist = ((c1_x-c2_x)**2 + (c1_y-c2_y)**2) ** 0.5

            if dist < 8*R/5:
                overlap_penalty += 10000
            elif dist <= 2*R:
                overlap_penalty += 1000

    umbrella_usage_penalty = num_of_used_umbrellas*10

    total_penalty = uncovered_penalty+overlap_penalty+umbrella_usage_penalty+more_points_covered

    return -total_penalty

gene_space = [{'low':R, 'high':10-R},{'low':R,'high':10-R}]*M


params = {
    'num_generations': 500,
    'sol_per_pop': 100,
    'num_parents_mating': 50,

    'num_genes': 2*M,
    'gene_space': gene_space,

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'save_best_solutions': True
}


ga = pygad.GA(**params)

ga.run()

solution, _, _ = ga.best_solution()
fitness = fitness_func(None, solution, 0)
best_solutions = ga.best_solutions

print(solution)
print(fitness)


# Part 2.
chromosomes = [
    [8.0,8.0,8.0,8.0,8.0,8.0],
    [1.0,1.0,8.0,8.0,8.0,8.0],
    [1.0,1.0,5.0,5.0,8.0,8.0],
    [5.0,5.0,6.0,6.0,1.0,1.0],
    [5.0,5.0,8.0,8.0,1.0,1.0]
]
for i,chrom in enumerate(chromosomes,1):
    print(f"Chromosome {i}: {fitness_func(None,chrom,0)}")

# submit_data(fitness_func, decode, chromosomes, best_solutions)