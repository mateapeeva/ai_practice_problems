from constraint import *

if __name__ == '__main__':

    bands = dict()

    band_info = input()
    while band_info != 'end':
        band, time, genre = band_info.split(' ')
        bands[band] = (time, genre)
        band_info = input()

    # Add the variables here
    variables = [band for band in bands.keys()]

    domain = [f'S{i + 1}' for i in range(3)]

    problem = Problem(BacktrackingSolver())

    # Change this section if necessary
    problem.addVariables(variables, domain)

    # Add the constraints here

    # Constraint 1: max one band == 120min
    for band1 in bands.keys():
        for band2 in bands.keys():
            if band1 != band2:
                time1 = int(bands[band1][1])
                time2 = int(bands[band2][1])
                if time1 == 120 and time2 == 120:
                    problem.addConstraint(AllDifferentConstraint(),[band1,band2])

    # Constraint 2: max 5 bands < 80min
    def constraint_2(*allvariables):
        counter = [0 for _ in range(4)]
        for var in allvariables:
            counter[int(var[1])] += 1

        for i in range(1,4):
            if counter[i] > 5:
                return False

        return True

    bands_less_80 = []
    for band in bands.keys():
        if int(bands[band][1]) < 80:
            bands_less_80.append(band)
    problem.addConstraint(constraint_2,bands_less_80)


    # Constraint 3: if per genre <= 300 -> same scene
    punk_count = 0
    rock_count = 0
    metal_count = 0
    punk = []
    rock = []
    metal = []

    for band in bands.keys():
        if bands[band][0] == 'punk':
            punk_count += int(bands[band][1])
            punk.append(band)
        elif bands[band][0] == 'rock':
            rock_count += int(bands[band][1])
            rock.append(band)
        else:
            metal_count += int(bands[band][1])
            metal.append(band)

    if 300 >= punk_count > 0:
        problem.addConstraint(AllEqualConstraint(),punk)
    if 300 >= rock_count > 0:
        problem.addConstraint(AllEqualConstraint(),rock)
    if 300 >= metal_count > 0:
        problem.addConstraint(AllEqualConstraint(),metal)


    result = problem.getSolution()

    # Add the printing section here
    res = sorted(result.keys(),key=lambda x: int(x[4:]))
    for band in res:
        print(f'{band} ({bands[band]}): {result[band]}')
