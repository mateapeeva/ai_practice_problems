from searching_framework import *

class Robot(Problem):
    def __init__(self,walls, initial,s1,s2, goal=None):
        super().__init__(initial, goal)
        self.grid_size = (10, 10)
        self.walls = walls
        self.s1 = s1
        self.s2 = s2

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        m1_fixed = state[3]==0
        m2_fixed = state[4]==0
        return m1_fixed and m2_fixed

    def successor(self, state):
        dir = {"Up": (0, +1), "Down": (0, -1), "Left": (-1, 0), "Right": (+1, 0)}

        successors = dict()
        #soberi parts m1 -> popravi m1 so m1_steps -> soberi m2 parts
        r_pos, m1_pos, m2_pos, m1_steps, m2_steps, m1_parts, m2_parts, m1_collect, m2_collect = state
        r_x, r_y = r_pos

        m1_fixed = m1_steps==0

        if m1_parts == 0 and r_pos == m1_pos and not m1_fixed:
            successors['Repair'] = (
                r_pos, m1_pos, m2_pos, m1_steps-1, m2_steps, m1_parts, m2_parts, m1_collect, m2_collect
            )
        if m1_fixed and r_pos == m2_pos and m2_parts == 0:
            successors['Repair'] = (
                r_pos, m1_pos, m2_pos, m1_steps, m2_steps - 1, m1_parts, m2_parts, m1_collect, m2_collect
            )

        for movement,(move_x,move_y) in dir.items():
            new_x, new_y = move_x+r_x, move_y+r_y
            r_pos_new = (new_x,new_y)
            new_m1_parts, new_m2_parts = m1_parts, m2_parts
            new_m1_steps, new_m2_steps = m1_steps, m2_steps
            new_m1_collect, new_m2_collect = m1_collect, m2_collect

            if r_pos_new in self.walls:
                continue
            if not (0<=new_x<self.grid_size[0] and 0<=new_y<self.grid_size[1]):
                continue
            if not m1_fixed and r_pos_new in m1_collect:
                new_m1_parts -= 1
                new_m1_collect = tuple([s for s in m1_collect if s != r_pos_new])
            elif m1_fixed and r_pos_new in m2_collect:
                new_m2_parts -= 1
                new_m2_collect = tuple([s for s in m2_collect if s != r_pos_new])

            if "Repair" in successors:
                new_m1_steps = self.s1

            successors[movement] = (
                r_pos_new, m1_pos, m2_pos, new_m1_steps, new_m2_steps, new_m1_parts, new_m2_parts, new_m1_collect, new_m2_collect
            )


        return successors

if __name__ == '__main__':
    robot_start_pos = tuple(map(int, input().split(',')))
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())
    parts_M1 = int(input())
    to_collect_M1 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M1)])
    parts_M2 = int(input())
    to_collect_M2 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M2)])

    walls = [(4, 0), (5, 0), (7, 5), (8, 5), (9, 5), (1, 6), (1, 7), (0, 6), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9)]

    problem = Robot(walls,(robot_start_pos,M1_pos,M2_pos,M1_steps,M2_steps,parts_M1,parts_M2,to_collect_M1,to_collect_M2),M1_steps,M2_steps)

    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No Solution!")
