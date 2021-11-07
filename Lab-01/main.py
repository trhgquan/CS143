#
#   COMMANDLINE: python3 main.py --input=<input_file>.txt --output=<output_file>
#
#   Code by ndthang01 ft. trhgquan
#

import sys, getopt
from utility import *
from implementation.DFS import *
from implementation.BFS import *
from implementation.greedy_bfs import *
from implementation.astar import *
from implementation.bonus import *

def main(argv):
    input_file, output_file, algorithm_used = '', '', ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o', ['input=', 'output=', 'algo='])
    except getopt.GetoptError:
        print('Command line arguments invalid, try again.')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--input':
            input_file = arg
        elif opt == '--output':
            output_file = arg
        elif opt == '--algo':
            algorithm_used = arg

    if (input_file == '' or output_file == ''):
        print('Arguments missing, try again.')
        sys.exit(2)

    bonus_points, matrix = Utility.read_file(input_file)
    start, end = Utility.get_start_end(matrix)

    route = []

    if algorithm_used == 'dfs':
        route = DFS(matrix, start, end).Try()
    elif algorithm_used == 'bfs':
        route = BFS(matrix, start, end).Try()
    elif algorithm_used == 'greedy':
        route = GreedyBFS(matrix, start, end).Try()
    elif algorithm_used == 'astar':
        route = AStar(matrix, start, end).Try()
    elif algorithm_used == 'bonus':
        route = Bonus(matrix, start, end, bonus_points).Try()
    else:
        print('Algorithm not specified. Printing the map without route to exit..')

    plt = Utility.visualize_maze(matrix, bonus_points, start, end, route)
    plt.savefig(output_file)

if __name__ == '__main__':
    main(sys.argv[1:])
