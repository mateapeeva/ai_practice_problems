from searching_framework import Problem, breadth_first_graph_search


class Goal(Problem):
    def __init__(self, initial, defenders, goal_pos, goal=None):
        super().__init__(initial, goal)
        self.defenders = defenders
        self.goal_pos = goal_pos

    def check_valid(self,state):
        man,ball = state
        man_x,man_y = man
        ball_x,ball_y = ball

        # Inside of grid?
        if man_x < 0 or man_x > 7 or man_y < 0 or man_y > 5:
            return False
        if ball_x < 0 or ball_x > 7 or ball_y < 0 or ball_y > 5:
            return False

        # Man vs Defender
        if man in self.defenders:
            return False

        # Ball vs Defender
        for (def_x,def_y) in self.defenders:
            if max(abs(def_x-ball_x),abs(def_y-ball_y)) <= 1:
                return False

        return True

    def successor(self, state):
        successors = {}
        man_pos, ball_pos = state
        movements = {"up":(0,1),"down":(0,-1),"right":(1,0),"up-right":(1,1),"down-right":(1,-1)}

        for move,(x,y) in movements.items():
            man_pos_new = (man_pos[0]+x,man_pos[1]+y)
            ball_pos_new = (ball_pos[0] + x, ball_pos[1] + y)
            if man_pos_new == ball_pos:
                if self.check_valid((man_pos_new,ball_pos_new)):
                    successors[f"Push ball {move}"] = (man_pos_new,ball_pos_new)
            else:
                if self.check_valid((man_pos_new,ball_pos)):
                    successors[f"Move man {move}"] = (man_pos_new,ball_pos)

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        man,ball = state
        return ball in self.goal_pos



if __name__ == '__main__':
    defenders = ((3,3),(5,4))
    goal = ((7,2),(7,3))
    man = tuple(map(int,input().split(',')))
    ball = tuple(map(int,input().split(',')))
    initial = (man,ball)

    problem = Goal(initial, defenders, goal)

    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
