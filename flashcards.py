import argparse
import sys
import random

def parse(file_name, separator):
    with open(file_name, 'r') as flashcards_file:
        result = []
        # Parsing file into 2D table
        for i in flashcards_file.readlines():
            i = i.rstrip().lstrip()
            if i != '':  # If line isn't empty
                result.append(i.split(separator))
                if len(result[-1]) < 2:
                    print('Error: Invalid line:', result[-1][0])
                    print('Skipping.')
                    result.pop()
        return result


# Argparse initialization
parser = argparse.ArgumentParser(description='Digital flashcards software.', epilog='File should contain two phrases separated by separator (default is "; ").')
parser.add_argument('-v', '--version', action='version', version='Flashcards 0.1')
parser.add_argument('-s', '--separator', default='; ', help='sets separator beetween showed and hidden word versions, e.g. ". "')
parser.add_argument('-r', '--reverse', action='store_true', help='reverses displayed and hidden names')
parser.add_argument('-l', '--reload', default='{reload}', help='sets file reload sequence (write it as an answer to reload file, default is "{reload}")')
parser.add_argument('file_name', help='name of file containing flashcards data')

# Argument parsing
if len(sys.argv) > 1:  # If enough command line arguments were given
    args = parser.parse_args(sys.argv[1:])  # Processing command line arguments
else:
    parser.parse_args([])  # Else processing empty list (help should be displayed)

try:
    flashcards = parse(args.file_name, args.separator)
        
    if args.reverse:
        displayed, hidden = 1, 0
    else:
        displayed, hidden = 0, 1

    remaining = [i for i in range(len(flashcards))]  # List with refferences to flashcards data

    # Main loop
    iteration = 0
    while len(remaining) > 0:
        iteration += 1
        print('Round ', iteration, ':', sep='')
        random.shuffle(remaining)
        i = 0
        while i < len(remaining):
            current = flashcards[remaining[i]]  # Current phrases pare
            answer = input(current[displayed] + ': ')

            if answer == args.reload:
                flashcards = parse(args.file_name, args.separator)
            elif answer == current[hidden]:
                print('Good answer.')
                remaining.pop(i)
            else:
                print('Wrong. The correct answer is:', current[hidden])
                print('                              ', end='')  # Printing indentation for error pointer
                for j in range(len(answer) if len(answer) > len(current[hidden]) else len(current[hidden])):  # For every character in answer
                    if j >= len(answer) or j >= len(current[hidden]) or answer[j] != current[hidden][j]:  # Checking if this is place of error
                        print('^')  # Printing error pointer
                        break
                    else:
                        print(' ', end='')  # Inreasing indentation

                i += 1
    print('Congratulations!')
except FileNotFoundError:
    print('Error: File not found')
except KeyboardInterrupt:
    print('Interrupted')
except:
    print('Error: Invalid file')
