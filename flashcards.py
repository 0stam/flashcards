import argparse
import sys
import random


class NoMatchingTagsError(Exception):  # Custom error
    pass


def parse(file_name, separator):
    with open(file_name, 'r') as flashcards_file:
        result = []
        tags = {}
        # Parsing file into 2D table
        for i in flashcards_file.readlines():
            i = i.strip()
            if i != '':  # If line isn't empty
                result.append(i.split(separator))
                if len(result[-1]) < 2:
                    if result[-1][0][0] == "#":  # If line is a tag
                        tags[result[-1][0][1:].strip()] = len(result) - 1
                    else:  # If line is incorrect
                        print('Error: Invalid line:', result[-1][0])
                        print('Skipping.')
                    result.pop()
        return result, tags


# Argparse initialization
parser = argparse.ArgumentParser(description='Digital flashcards software.', epilog='File should contain two phrases separated by separator (default: "; ") in each line.')
parser.add_argument('-v', '--version', action='version', version='Flashcards 0.3')
parser.add_argument('-s', '--separator', default='; ', help='set separator beetween showed and hidden word versions, e.g. ". "')
parser.add_argument('-r', '--reverse', action='store_true', help='reverse displayed and hidden names')
parser.add_argument('-l', '--reload', default='{reload}', help='set file reload sequence (write it as an answer to reload file, default is "{reload}")')
parser.add_argument('-t', '--tag', action='append', help='by putting line "#x" before the block of text, you make it belong to the tag "x"; ' +
                                                         'than you can start the test including only words from selected tags by running e.g. "flashcards -t part1 -t part2 file_name')
parser.add_argument('file_name', help='name of file containing flashcards data')

# Argument parsing
if len(sys.argv) > 1:  # If enough command line arguments were given
    args = parser.parse_args(sys.argv[1:])  # Processing command line arguments
else:
    parser.parse_args([])  # Else processing empty list (help should be displayed)

try:
    flashcards, tags = parse(args.file_name, args.separator)
        
    if args.reverse:
        displayed, hidden = 1, 0
    else:
        displayed, hidden = 0, 1
    
    remaining = []  # List with refferences to flashcards data
    if args.tag:  # If tags were selected
        possible_tags = list(tags.keys())
        for i in args.tag:
            if not i in possible_tags:
                print('Error: Invalid tag:', i)
                continue

            position = possible_tags.index(i)
            if position == len(possible_tags) - 1:  # If this is the last tag, add indexes to the very end
                remaining += [j for j in range(tags[i], len(flashcards))]
            else:  # Else add indexes from this tag to the next one
                remaining += [j for j in range(tags[i], tags[possible_tags[position + 1]])]

        if not remaining:  # If no tags were found, raise error
            raise NoMatchingTagsError
    else:  # If no tags were selected, add all indexes
        remaining = [i for i in range(len(flashcards))]

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
                flashcards, _ = parse(args.file_name, args.separator)
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
    print('\nInterrupted')
except NoMatchingTagsError:
    print("Error: No matching tags found")
except:
    print('Error: Invalid file')
