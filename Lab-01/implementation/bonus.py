from .IAlgorithm import *

'''
So the basic idea here is to assume bonuses as negative edges in a graph.
With negative edges, first thing appears in our mind is Bellman-Ford algorithm.

But sadly A* and Bellman-Ford cannot co-exist at the same time.
So we created a light version of Bellman-Ford, using BFS with some memorisation.
'''

class Bonus(IAlgorithm):
    def __init__(self, matrix, start, end, bonus_points):
        super().__init__(matrix, start, end)
        self.bonus_points = dict()

        for x, y, w in bonus_points:
            if (x, y) not in self.bonus_points:
                self.bonus_points[(x, y)] = w

    def heuristic(self, start, end):
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        if end in self.bonus_points:
            return self.bonus_points[end]

        return abs(x1 - x2) + abs(y1 - y2) + abs(self.bonus_points[min(self.bonus_points.keys(), key = (lambda k : self.bonus_points[k]))])

    def Try(self):
        waiting = deque()
        waiting.append(self.start)

        trace, cost = dict(), dict()
        trace[self.start], cost[self.start] = None, 0

        while len(waiting) != 0:
            current = waiting.popleft()

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])

                if not self.inside(next):
                    continue

                new_cost = cost[current] + self.heuristic(current, next)

                if (next not in cost) or (new_cost < cost[next]):
                    cost[next] = new_cost
                    waiting.append(next)
                    trace[next] = current

        return self.create_route(trace)
