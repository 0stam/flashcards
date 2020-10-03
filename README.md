# Flashcards
Flashcards softwer made to support learning.

Version 0.2
### Usage
Create plain text file and write one pair of e.g. translations in one row separated by "; ".
You can then run `python flashcards.py filename` to start test.

First round tests all the words from the file, and each following containing words that waren't answered properly yet. When every phrase is answered right, test ends.

For more information run program with `-h` argument.
### Features
Besides basic functionality following features are also supported:
* reversing hidden and shown phrases,
* setting custom separator,
* reloading file during runtime.
