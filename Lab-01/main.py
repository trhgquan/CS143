#
#   COMMANDLINE: python3 main.py --input=<input_file>.txt --output=<output_file>
#
#   Code by ndthang01 ft. trhgquan
#

import sys, getopt
from utility import *

# BO SUNG IMPORT THU VIEN O DAY


###############################

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

    if (input_file == '' or output_file == '' or algorithm_used == ''):
        print('Arguments missing, try again.')
        sys.exit(2)

    bonus_points, matrix = Utility.read_file(input_file)
    start, end = Utility.get_start_end(matrix)

    route = []
    # BO SUNG HAM GOI THUAT TOAN O DAY
    if algorithm_used == 'dfs':
        pass
    elif algorithm_used == 'bfs':
        pass
    elif algorithm_used == 'greedy':
        pass
    elif algorithm_used == 'astar':
        pass
    elif algorithm_used == 'bonus':
        pass
    else:
        print('Algorithm not specified.')

    ##################################


    plt = Utility.visualize_maze(matrix, bonus_points, start, end, route)
    plt.savefig(output_file)

if __name__ == '__main__':
    main(sys.argv[1:])
