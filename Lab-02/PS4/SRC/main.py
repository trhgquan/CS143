import os
from resolution import logic_resolution

INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

def main():
    # Walkthrough files inside input directory.
    # Credit: https://stackoverflow.com/a/3207973
    file_list = next(os.walk(INPUT_DIR), (None, None, []))[2]

    # Create output directory.
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    for file in file_list:
        input_file = INPUT_DIR + file
        output_file = OUTPUT_DIR + file.replace('input', 'output')

        with open(input_file, 'r+') as f:
            try:
                alpha = f.readline().strip()
                n = int(f.readline().strip())
                kb = []
                for i in range(n):
                    clause = f.readline().strip()
                    kb.append(clause)
            except:
                print('Error processing', input_file, ', maybe the file is empty?')
                continue

        resolver = logic_resolution(kb, alpha)
        resolver.pl_resolution()

        with open(output_file, 'w+') as f:
            resolver.print_output(f = f)
        print('Solved', input_file, ', wrote to', output_file)

if __name__ == '__main__':
    main()