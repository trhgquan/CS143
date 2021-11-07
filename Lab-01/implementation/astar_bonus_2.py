from .greedy_bfs import *
from .astar import *
class AStar_bonus_2(GreedyBFS):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self,bonus_points):
        waiting = PriorityQueue()
        waiting.put(self.start, 0)

        trace, cost = dict(), dict()
        trace[self.start], cost[self.start] = None, 0
        
        bonus_dict = dict()
        # use astar from bonus to exit : find cost
        for point in bonus_points:
            point_pos = point[0:2]
            route = AStar(self.matrix,point_pos,self.end).Try()
            bonus_dict[point_pos] = route

        while not waiting.empty():
            current = waiting.get()

            if (current == self.end):
                break

            #cost from current to bonus
            for point in bonus_points:
                if self.heuristic(current, point) <= abs(point[2]):
                    bonus_point = point[0:2]
                    route_to_bonus = AStar(self.matrix, current, bonus_point).Try()
                    trace[self.end] = bonus_dict[bonus_point] + trace[bonus_point]
                    break
            if trace[self.end] != None: break

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
