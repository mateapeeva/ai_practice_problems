import pygad


def read_input():
    M, N = map(int, input().split())
    K = int(input())
    B = int(input())

    unusable = set()
    for _ in range(B):
        r, c = map(int, input().split())
        unusable.add((r, c))

    return M, N, K, unusable


def fitness_func(ga_instance, solution, solution_idx):
    sprinkles = list(set((int(element) for element in solution )))
    num_sprinkles = len(sprinkles)

    sprinkles_coordinates = []

    for sprinkle in sprinkles:
        r,c = sprinkle//N, sprinkle%N
        sprinkles_coordinates.append((r,c))

    crops_covered = set()

    rhomb_offsets = [(-2, 0), (-1, -1), (-1, 0), (-1, 1), (0, -2), (0, -1), (0, 1), (0, 2), (1, -1), (1, 0), (1, 1), (2, 0)]

    for r,c in sprinkles_coordinates:
        for add_r,add_c in rhomb_offsets:
            crop_r, crop_c = r+add_r, c+add_c
            if 0 <= crop_r < M and 0 <= crop_c < N:
                crop = (crop_r,crop_c)
                if crop not in sprinkles_coordinates and crop not in unusable:
                    crops_covered.add(crop)

    num_crops_covered = len(crops_covered)

    return num_crops_covered - num_sprinkles




if __name__ == "__main__":
    M, N, K, unusable = read_input()

    gene_space = list(range(N*M))

    params = {
        'num_generations': 100,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': K,
        'gene_space': gene_space,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    rhomb_offsets = [(-2, 0), (-1, -1), (-1, 0), (-1, 1), (0, -2), (0, -1), (0, 1), (0, 2), (1, -1), (1, 0), (1, 1), (2, 0)]
    sprinkler_set = set(best_solution)
    fitness = fitness_func(None,best_solution,0)

    print(f"Number of watered crops: {len(sprinkler_set)+fitness}")
    print(f"Number of sprinklers: {len(sprinkler_set)}")
    for index in sprinkler_set:
        x,y = index//N, index%N
        print(f"Position of sprinkler: {x}, {y}")