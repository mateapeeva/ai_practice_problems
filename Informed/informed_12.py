from math import ceil

from searching_framework import Problem, astar_search, breadth_first_graph_search

class Climbing(Problem):
    def __init__(self, initial, allowed, goal=None):
        super().__init__(initial, goal)
        self.allowed = allowed

    def goal_test(self, state):
        man_pos,house_pos,house_dir = state
        return man_pos == house_pos

    def check_valid(self,state):
        man_pos,house_pos = state
        man_x,man_y = man_pos

        if man_x < 0 or man_x > 4 or man_y < 0 or man_y > 8:
            return False
        if (man_x,man_y) not in self.allowed and man_pos != house_pos:
           return False

        return True

    def h(self, node):
        man_pos, house_pos, house_dir = node.state

        return max(abs(man_pos[0]-house_pos[0])//2,abs(man_pos[1]-house_pos[1])//2)

    def successor(self, state):
        succ = {}
        movement = {"Up 1":(0,1),"Up 2":(0,2),"Up-left 1":(-1,1),"Up-right 1":(1,1),"Up-left 2":(-2,2),"Up-right 2":(2,2),"Wait":(0,0)}
        man_pos,house_pos,house_dir = state
        for move,(x,y) in movement.items():
            man_pos_new = (man_pos[0]+x,man_pos[1]+y)
            house_pos_new = (house_pos[0],house_pos[1])
            house_dir_new = house_dir
            if house_dir == "right":
                if house_pos[0]+1<5:
                    house_pos_new = (house_pos_new[0]+1,house_pos_new[1])
                else:
                    house_pos_new = (house_pos_new[0]-1,house_pos_new[1])
                    house_dir_new = "left"
            else:
                if house_pos[0]-1>=0:
                    house_pos_new = (house_pos_new[0]-1,house_pos_new[1])
                else:
                    house_pos_new = (house_pos_new[0]+1,house_pos_new[1])
                    house_dir_new = "right"

            if self.check_valid((man_pos_new,house_pos_new)):
                succ[move] = (man_pos_new,house_pos_new,house_dir_new)


        return succ

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

if __name__ == '__main__':
    allowed = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7)]

    man = tuple(map(int,input().split(',')))
    house = tuple(map(int,input().split(',')))
    house_dir = input()

    initial = (man,house,house_dir)

    problem = Climbing(initial,allowed)

    result = astar_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")

