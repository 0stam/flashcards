# Flashcards
Flashcards software made to support learning.

Version 0.3
### Usage
Create a plain text file following this order:
```
# part1
word1; translation
word2; translation

# part2
word3; translation
word4; tranlation
```

then run the program: `python flashcards.py [optional arguments] file_name`. 

When the program is run, it takes all word pairs separated by the "; ", shuffles them and shows the first word to the user, who then has to input the proper translation. When all words have been tested, the program proceeds to the next round containing all the words which haven't been answered properly yet. This process repeats until all correct answers were given.

Lines staring with "#" create tags. All words from this line to the next one containing a tag (or to the end of the file) belong to this tag. You can then specify which tags you want to include using `-t` argument. Tags overwrite their previous occurrences.

Blank lines are ignored.

For more information, run program with `-h` argument.
### Features
Besides basic functionality, following features are also supported:
* reversing the hidden and the shown phrases,
* setting a custom separator,
* reloading the file during runtime.
