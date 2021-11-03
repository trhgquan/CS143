from .IAlgorithm import *

class DFS(IAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self):
        reached, waiting = [], []
        trace = dict()

        trace[self.start] = None
        reached.append(self.start)
        waiting.append(self.start)

        while len(waiting) != 0:
            current = waiting[-1]
            reached.append(current)
            waiting.pop()

            if (current == self.end):
                break

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])

                if self.inside(next):
                    if next not in reached:
                        waiting.append(next)
                        trace[next] = current

        return self.create_route(trace)
