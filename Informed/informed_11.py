from searching_framework import Problem, astar_search
class Man(Problem):
    def __init__(self, initial, obstacles, n, goal=None):
        super().__init__(initial, goal)
        self.obstacles = obstacles
        self.goal = goal

    def check_valid(self, state):
        man = state
        if man in self.obstacles:
            return False
        if not 0 <= man[0] < n or not 0 <= man[1] < n:
            return False

        return True

    def successor(self, state):
        succ = {}
        movement = {"Right":(1, 0),"Up":(0, 1), "Down":(0, -1), "Left":(-1, 0)}
        man_pos = state

        for move,(x,y) in movement.items():
            new_man = (man_pos[0] + x, man_pos[1] + y)
            if move == "Right" and self.check_valid(new_man):
                for i in range(2):
                    new_man = (new_man[0]+x, new_man[1]+y)
                    if self.check_valid(new_man):
                        succ[f"{move} {i+2}"] = (new_man)
                    else:
                        break
            else:
                if self.check_valid(new_man):
                    succ[f"{move}"] = (new_man)

        return succ

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        man = node.state
        house = self.goal
        if man[0] < house[0]:
            value = abs(man[0] - house[0])/3 + abs(man[1] - house[1])
        else:
            value = abs(man[0] - house[0]) + abs(man[1] - house[1])

        return value

if __name__ == '__main__':
    n = int(input())
    num_obs = int(input())
    obstacles = []
    for _ in range(num_obs):
        obstacles.append(tuple(map(int, input().split(','))))
    man = tuple(map(int, input().split(',')))
    house = tuple(map(int, input().split(',')))

    initial = man
    goal = house

    problem = Man(initial, obstacles, n, goal)

    result = astar_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print('No solution')
