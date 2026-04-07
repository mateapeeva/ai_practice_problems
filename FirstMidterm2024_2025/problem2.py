import math

from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    movies = dict()

    n = int(input())
    for _ in range(n):
        film_info = input()
        film, genre, time = film_info.split(' ')
        movies[film] = (float(time), genre)

    l_days = int(input())

    # Tuka definirajte gi promenlivite i domenite
    variables = [film for film in movies.keys()]
    domains = [(d,t,c) for d in range(1,l_days+1) for t in range(12,24) for c in range(1,3)]


    # Tuka dodadete gi ogranichuvanjata
    # Children before 18
    for var in variables:
        genre = movies[var][1]
        if genre == "children's":
            available = []
            for domain in domains:
                domain_t = domain[1]
                if domain_t <= 18:
                    available.append(domain)
            problem.addVariable(var, available)
        else:
            problem.addVariable(var, domains)


    # Do not overlap
    def overlap(slot1, slot2, dur1, dur2):
        time1 = slot1[1]
        time2 = slot2[1]
        if slot1[0] == slot2[0] and slot1[2] == slot2[2]:
            end1 = time1 + dur1
            end2 = time2 + dur2
            return end1 < time2 or end2 < time1

        return True


    for film1 in variables:
        for film2 in variables:
            if film2 < film1:
                dur1 = movies[film1][0]
                dur2 = movies[film2][0]
                problem.addConstraint(lambda f1, f2, d1=dur1, d2=dur2: overlap(f1, f2, d1, d2), (film1, film2))

    # Same Cinema
    for film1 in variables:
        for film2 in variables:
            if film2 < film1:
                genre1 = movies[film1][1]
                genre2 = movies[film2][1]
                if genre1 == genre2 and (genre1 == "sci-fi" or genre1 == "horror" or genre1 == "action"):
                    problem.addConstraint(lambda f1, f2: f1[2] == f2[2], (film1, film2))

    # All diff
    problem.addConstraint(AllDifferentConstraint(),variables)

    result = problem.getSolution()

    # Tuka dodadete go kodot za pechatenje
    if result:
        for film in movies.keys():
            print(f"{film}: Day {result[film][0]} {result[film][1]}:00 - Cinema {result[film][2]}")
    else:
        print("No Solution!")

