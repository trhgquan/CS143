from os import walk
from resolution import logic_resolution

INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

def main():
    # Walkthrough files inside input directory.
    # Credit: https://stackoverflow.com/a/3207973
    filenames = next(walk(INPUT_DIR), (None, None, []))[2]

    for file in filenames:
        with open(INPUT_DIR + file, 'r+') as f:
            alpha = f.readline().strip()
            n = int(f.readline().strip())
            kb = []
            for i in range(n):
                clause = f.readline().strip()
                kb.append(clause)

        resolver = logic_resolution(kb, alpha)
        resolver.pl_resolution()
        with open(OUTPUT_DIR + file, 'w+') as f:
            resolver.print_output(f = f)
        print('Solved:', file)

if __name__ == '__main__':
    main()