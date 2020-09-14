import argparse
import sys
import random

# Argparse initialization
parser = argparse.ArgumentParser(description="Digital flashcards software.", epilog='File should contain two phrases separated by separator (default is "; ").')
parser.add_argument('-v', '--version', action='version', version='Flashcards 0.1')
parser.add_argument('-s', '--separator', default="; ", help='sets separator beetween showed and hidden word versions, e.g. ". "')
parser.add_argument('-r', '--reverse', action='store_true', help='reverses displayed and hidden names')
parser.add_argument('file_name', help='name of file containing flashcards data')

# Argument parsing
if len(sys.argv) > 1:  # If enough command line arguments were given
    args = parser.parse_args(sys.argv[1:])  # Processing command line arguments
else:
    parser.parse_args([])  # Else processing empty list (help should be displayed)

# Opening file
try:
    with open(args.file_name, 'r') as flashcards_file:
        flashcards = []
        if args.reverse:
            displayed, hidden = 1, 0
        else:
            displayed, hidden = 0, 1
        
        # Parsing file into 2D table
        for i in flashcards_file.readlines():
            i = i.rstrip().lstrip()
            if i != "":  # If line isn't empty
                flashcards.append(i.split(args.separator))
                if len(flashcards[-1]) < 2:
                    print('Error: Invalid line:', flashcards[-1][0])
                    print('Skipping.')
                    flashcards.pop()

        # Main Loop
        while len(flashcards) > 0:
            random.shuffle(flashcards)
            i = 0
            while i < len(flashcards):
                answer = input(flashcards[i][displayed] + ': ')
                if answer == flashcards[i][hidden]:
                    print('Good answer.')
                    flashcards.pop(i)
                else:
                    print('Wrong. Correct answer is:', flashcards[i][hidden])
                    i += 1
        print('Congratulations!')
except FileNotFoundError:
    print('Error: File not found')
except KeyboardInterrupt:
    print('Interrupted.')
except:
    print('Error: Invalid file.')
