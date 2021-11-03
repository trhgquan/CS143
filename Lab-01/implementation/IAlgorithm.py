from collections import deque

class IAlgorithm:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.start = start
        self.end = end
        self.wall_char = 'x'
        self.steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def inside(self, point):
        return (point[0] < len(self.matrix) and point[0] >= 0 and
            point[1] < len(self.matrix[0]) and point[1] >= 0 and
            self.matrix[point[0]][point[1]] != self.wall_char)

    def create_route(self, trace):
        current = self.end
        path = []

        while current != self.start:
            path.append(current)
            current = trace[current]

        path.append(self.start)
        path.reverse()

        return path

    def Try(self):
        pass
