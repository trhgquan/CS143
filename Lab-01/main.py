#
#   COMMANDLINE: python3 main.py --input=<input_file>.txt --output=<output_file.txt>
#
#   Code by ndthang01 ft. trhgquan
#

import sys, getopt
from utility import *

# BO SUNG IMPORT THU VIEN O DAY

###############################

def main(argv):
    input_file, output_file = '', ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o', ['input=', 'output='])
    except getopt.GetoptError:
        print('Command line arguments invalid, try again.')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--input':
            input_file = arg
        elif opt == '--output':
            output_file = arg

    if (input_file == '' or output_file == ''):
        print('Arguments missing, try again.')
        sys.exit(2)

    bonus_points, matrix = Utility.read_file(input_file)
    start, end = Utility.get_start_end(matrix)

    # BO SUNG HAM GOI THUAT TOAN O DAY



    ##################################


    plt = Utility.visualize_maze(matrix, bonus_points, start, end)
    plt.savefig(output_file)

if __name__ == '__main__':
    main(sys.argv[1:])
