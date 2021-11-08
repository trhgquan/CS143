from .greedy_bfs import *

class AStar(GreedyBFS):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self):
        waiting = PriorityQueue()
        waiting.put(self.start, 0)

        trace, cost = dict(), dict()
        trace[self.start], cost[self.start] = None, 0

        while not waiting.empty():
            current = waiting.get()

            if (current == self.end):
                break

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])

                if not self.inside(next):
                    continue

                new_cost = cost[current] + self.heuristic(current, self.end)

                if (next not in cost) or (new_cost < cost[next]):
                    cost[next] = new_cost
                    waiting.put(item = next, priority = new_cost)
                    trace[next] = current

        return self.create_route(trace)
