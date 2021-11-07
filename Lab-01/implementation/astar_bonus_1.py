from .greedy_bfs import *
from .astar import *
class AStar_bonus_1(GreedyBFS):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self,bonus_points):
        waiting = PriorityQueue()
        waiting.put(self.start, 0)

        trace, cost = dict(), dict()
        trace[self.start], cost[self.start] = None, 0
        

        while not waiting.empty():
            current = waiting.get()

            if (current == self.end):
                break

            #cost from current to bonus
            for point in bonus_points:
                if self.heuristic(current, point) <= abs(point[2]):
                    bonus_point = point[0:2]
                    route_to_bonus = AStar(self.matrix, current, bonus_point).Try()
                    new_cost = cost[current] + len(route_to_bonus) - point[2]
                    cost[bonus_point] = new_cost
                    waiting.put(item = bonus_point, priority = new_cost)
                    trace[bonus_point] = route_to_bonus
                    continue

            for step in self.steps:
                next = (current[0] + step[0], current[1] + step[1])

                if not self.inside(next):
                    continue

                new_cost = cost[current] + self.heuristic(current, next)

                if (next not in cost) or (new_cost < cost[next]):
                    cost[next] = new_cost
                    waiting.put(item = next, priority = new_cost)
                    trace[next] = current

        return self.create_route(trace)
