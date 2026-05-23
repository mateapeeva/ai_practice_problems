import pygad
from sklearn.tree import DecisionTreeClassifier

dataset = [
    [2, 3, 1, 7, 0],
    [5, 6, 4, 3, 1],
    [1, 1, 2, 8, 1],
    [7, 8, 6, 4, 1],
    [3, 2, 1, 9, 0],
    [8, 7, 5, 2, 1],
    [4, 5, 2, 6, 1],
    [1, 3, 1, 9, 0],
    [9, 8, 7, 2, 1],
    [2, 2, 3, 8, 0],
    [6, 5, 4, 3, 1],
    [1, 0, 2, 9, 0],
    [7, 7, 6, 5, 1],
    [2, 1, 1, 8, 0],
    [8, 9, 5, 3, 1],
    [3, 4, 2, 7, 0],
    [5, 5, 5, 4, 0],
    [0, 1, 1, 9, 0],
    [9, 9, 8, 1, 1],
    [2, 3, 2, 7, 0],
    [6, 7, 5, 3, 1],
    [1, 2, 0, 8, 0],
    [8, 6, 7, 2, 0],
    [3, 1, 2, 9, 0],
    [7, 5, 6, 4, 1],
    [2, 0, 1, 8, 0],
    [9, 7, 8, 2, 1],
    [4, 3, 2, 7, 0],
    [6, 6, 5, 4, 1],
    [1, 1, 0, 9, 0],
    [8, 8, 6, 3, 1],
    [2, 2, 1, 8, 0],
    [7, 9, 5, 2, 1],
    [3, 2, 2, 7, 0],
    [5, 7, 4, 3, 1],
    [0, 1, 2, 9, 0],
    [9, 8, 6, 2, 0],
    [2, 3, 1, 8, 0],
    [6, 5, 5, 4, 1],
    [1, 0, 1, 9, 0],
    [8, 7, 7, 2, 1],
    [3, 1, 1, 8, 0],
    [7, 6, 5, 3, 0],
    [2, 2, 0, 9, 0],
    [9, 9, 7, 1, 1],
    [4, 2, 2, 7, 0],
    [6, 8, 5, 2, 1],
    [1, 1, 1, 8, 1],
    [8, 6, 6, 3, 1],
    [2, 0, 2, 9, 1],
    [7, 7, 5, 4, 1],
    [3, 2, 1, 8, 0],
    [9, 8, 8, 2, 1],
    [1, 0, 0, 9, 0],
    [6, 6, 4, 3, 1],
    [2, 1, 2, 8, 0],
    [8, 9, 6, 2, 1],
    [4, 3, 1, 7, 0],
    [7, 5, 5, 4, 1],
    [1, 2, 1, 9, 0],
    [9, 7, 6, 1, 1],
    [2, 2, 2, 8, 0],
    [6, 8, 7, 3, 1],
    [0, 1, 1, 8, 0],
    [8, 8, 5, 2, 1],
    [3, 2, 0, 9, 0],
    [7, 6, 6, 4, 1],
    [1, 1, 2, 8, 0],
    [9, 9, 5, 1, 1],
    [2, 3, 0, 9, 0],
    [6, 7, 6, 3, 1],
    [1, 0, 1, 8, 0],
    [8, 7, 5, 3, 1],
    [3, 1, 0, 9, 0],
    [7, 8, 7, 2, 1],
    [2, 2, 1, 9, 0],
    [9, 6, 8, 1, 1],
    [4, 2, 1, 8, 0],
    [6, 5, 6, 4, 1],
    [1, 1, 0, 8, 0]
]

X,y = [row[:-1] for row in dataset],[row[-1] for row in dataset]

split_index = int(len(X)*0.75)

train_X, train_y = X[:split_index], y[:split_index]
test_X, test_y = X[split_index:], y[split_index:]

def decode(solution):
    criterion, max_depth, min_samples_split, max_leaf_nodes = criterion_dict.get(solution[0]), int(solution[1]), int(solution[2]), int(solution[3])
    params = {
        'criterion': criterion,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'max_leaf_nodes': max_leaf_nodes,
    }

    return params

def fitness_func(ga_instance, solution, solution_idx):
    params = decode(solution)

    criterion, max_depth, min_samples_split, max_leaf_nodes = [params.get(key) for key in params.keys()]

    classifier = DecisionTreeClassifier(**params)
    classifier.fit(train_X,train_y)

    accuracy = classifier.score(test_X,test_y)

    fitness = accuracy*10000 - max_depth*10 - max_leaf_nodes*10

    return fitness


criterion_dict = {1:'gini',2:'entropy'}

# criterion, max_depth, min_samples_split, max_leaf_nodes
gene_space = [[1,2], [5, 10, 15, 20, 25], [2, 3, 4, 5, 10], [5, 10, 15, 20, 25]]

ga_instance = pygad.GA(
    num_generations=40,
    sol_per_pop=50,
    num_parents_mating=25,
    fitness_func=fitness_func,
    num_genes=4,
    gene_space=gene_space,
    mutation_num_genes=1
)

ga_instance.run()
best_solution, _, _ = ga_instance.best_solution()

params = decode(best_solution)

classifier = DecisionTreeClassifier(**params)
classifier.fit(train_X, train_y)
accuracy = classifier.score(test_X, test_y)

for key in params.keys():
    print(f"{key}: {params.get(key)}")
print(f"accuracy: {accuracy}")
