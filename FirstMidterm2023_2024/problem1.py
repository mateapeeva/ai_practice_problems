from searching_framework import *


# from utils import *
# from uninformed_search import *
# from informed_search import *

class Boxes(Problem):
    def __init__(self, initial,n,boxes, goal=None):
        super().__init__(initial, goal)
        self.n = n
        self.boxes = boxes

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        boxes = state[1]
        return len(boxes) == 0

    def check_valid(self,state):
        man = state
        if man in self.boxes:
            return False
        if not 0 <= man[0] < self.n or not 0 <= man[1] < self.n:
            return False

        return True

    def successor(self, state):
        succ = {}
        actions = {"Gore":(0,1),"Desno":(1,0)}
        man,boxes = state

        def chebishev(man,box):
            return max(abs(man[0] - box[0]), abs(man[1] - box[1]))

        for action,(x,y) in actions.items():
            man_new = (man[0] + x, man[1] + y)
            boxes_new = set(item for item in boxes)

            if self.check_valid(man_new):
                for box in boxes:
                    if chebishev(man_new, box) == 1:
                        boxes_new.remove(box)
                        succ[action] = (man_new, tuple(boxes_new))

                succ[action] = (man_new, tuple(boxes_new))

        return succ


if __name__ == '__main__':
    n = int(input())
    man_pos = (0, 0)

    num_boxes = int(input())
    boxes = list()
    for _ in range(num_boxes):
        boxes.append(tuple(map(int, input().split(','))))

    problem = Boxes((man_pos, tuple(boxes)),n,boxes)

    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
