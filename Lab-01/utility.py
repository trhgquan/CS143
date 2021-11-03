import matplotlib.pyplot as plt

class Utility:
    # Read a file from filename, return bonus points and matrix
    def read_file(filename):
        bonus_points, matrix = [], []
        with open(filename) as f:
            n_bonus_points = int(next(f)[:-1])
            bonus_points = []

            for i in range(n_bonus_points):
                x, y, reward = map(int, next(f)[:-1].split(' '))
                bonus_points.append((x, y, reward))

            text = f.read()
            matrix = [list(i) for i in text.splitlines()]

        return bonus_points, matrix

    # Get starting and ending of a matrix
    def get_start_end(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'S':
                    start = (i, j)
                elif matrix[i][j] == ' ':
                    if (i == 0) or (i == len(matrix) - 1) or (j == len(matrix[0]) - 1) or (j == 0):
                        end = (i, j)
                else:
                    pass
        return start, end

    def visualize_maze(matrix, bonus, start, end, route = None):
        # 1. Define the walls and array of direction based on the route
        walls = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == 'x']

        if route:
            direction = []
            for i in range(1, len(route)):
                if route[i][0] - route[i - 1][0] > 0:
                    direction.append('v')
                if route[i][0] - route[i - 1][0] < 0:
                    direction.append('^')
                if route[i][1] - route[i - 1][1] > 0:
                    direction.append('>')
                if route[i][1] - route[i - 1][1] < 0:
                    direction.append('<')

            direction.pop(0)

        # 2. Drawing the map
        ax = plt.figure(dpi = 100).add_subplot(111)

        for i in ['top', 'bottom', 'right', 'left']:
            ax.spines[i].set_visible(False)

        plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                    marker = 'X', s = 10, color = 'black')

        plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                    marker = 'P', s = 10, color = 'green')

        plt.scatter(start[1], -start[0], marker = '*', s = 10, color = 'gold')

        if route:
            for i in range(len(route) - 2):
                plt.scatter(route[i + 1][1], -route[i + 1][0],
                marker = direction[i], s = 10, color = 'silver')

        plt.text(end[1], -end[0], 'EXIT', color = 'red',
                 horizontalalignment = 'center',
                 verticalalignment = 'center')

        plt.xticks([])
        plt.yticks([])

        return plt
