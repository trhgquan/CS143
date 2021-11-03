from .IAlgorithm import *
from .lib.PriorityQueue import *

class GreedyBFS(IAlgorithm):
    def heuristic(self, start, end):
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        return abs(x1 - x2) + abs(y1 - y2)

    def Try(self):
        waiting = PriorityQueue()
        waiting.put(self.start, 0)

        trace = dict()
        trace[self.start] = None

        while not waiting.empty():
            current = waiting.get()

            if (current == self.end):
                break

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])

                if not self.inside(next):
                    continue

                if (next not in trace):
                    waiting.put(item = next, priority = self.heuristic(next, self.end))
                    trace[next] = current

        return self.create_route(trace)
