from collections import deque
from .lib.PriorityQueue import *

class GreedyBFS:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.start = start
        self.end = end
        self.wall_char = 'x'
        self.steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def heuristic(self, start, end):
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        return abs(x1 - x2) + abs(y1 - y2)

    def inside(self, point):
        return point[0] < len(self.matrix) and point[0] >= 0 and point[1] < len(self.matrix[0]) and point[1] >= 0

    def create_route(self, trace):
        current = self.end
        path = []

        while (current != self.start):
            path.append(current)
            current = trace[current]

        path.append(self.start)
        path.reverse()

        return path

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

                if (self.matrix[next[0]][next[1]] != self.wall_char):
                    print(next, self.matrix[next[0]][next[1]])

                    if (next not in trace):
                        waiting.put(item = next, priority = self.heuristic(next, self.end))
                        trace[next] = current

        return self.create_route(trace)
