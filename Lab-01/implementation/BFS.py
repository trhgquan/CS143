from .IAlgorithm import *

class BFS(IAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self):
        frontier, reached = deque(), []
        frontier.append(self.start)
        reached.append(self.start)

        trace = dict()
        trace[self.start] = None

        while len(frontier) != 0:
            current = frontier.popleft()

            if (current == self.end): break

            neighbors = []

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])
                if self.inside(next):
                    neighbors.append(next)

            for next in neighbors:
                if next not in reached:
                    trace[next] = current
                    frontier.append(next)
                    reached.append(next)

        return self.create_route(trace)
