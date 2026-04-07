from searching_framework import *


class Laser(Problem):
    def __init__(self, initial, blocked,n,m, goal):
        super().__init__(initial, goal)
        self.blocked = blocked
        self.n = n
        self.m = m

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        man = state[0]
        return man == self.goal


    def successor(self, state):

        def laser_shoot(state):
            man, laser = state
            if man[0] == laser[0] or man[1] == laser[1]:
                return True
            return False

        def valid_pos(state):
            man = state
            if man in self.blocked:
                return False
            if not 0<=man[0]<self.m or not 0<=man[1]<self.n:
                return False
            return True

        succ = {}
        movements = {"Gore":(0,+1),"Dolu":(0,-1),"Levo":(-1,0),"Desno":(+1,0),"Stoj":(0,0)}
        man,laser,timer = state

        for action,(x,y) in movements.items():
            new_man = (man[0]+x,man[1]+y)
            new_laser = laser
            new_timer = timer+1

            if not valid_pos(new_man):
                continue
            else:
                if new_timer > 4:
                    new_timer = 1
                if new_timer == 1:
                    new_laser = new_man
                if new_timer == 4:
                    if laser_shoot((new_man,new_laser)):
                        continue

                succ[action] = (new_man,new_laser,new_timer)

        return succ


read_two = lambda: tuple(map(int, input().split()))
if __name__ == '__main__':
    N, M = read_two()
    man_pos = read_two()
    target_pos = read_two()
    timer = int(input())
    laser_pos = read_two()
    blocked = [read_two() for _ in range(int(input()))]
    initial = (man_pos,laser_pos,timer)

    problem = Laser(initial,blocked,N,M,target_pos)

    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
