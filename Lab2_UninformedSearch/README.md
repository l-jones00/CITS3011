# Lab 2: Uninformed Search

Using Python, implement a function `find_path` that, given a `start_word` (string), an `end_word` (string), and a `word_list` (list of strings, containing valid English words), finds the *shortest* sequence of words such that:
* The first word in the sequence is `start_word`
* The last word in the sequence is `end_word`
* Each word is in the `word_list`
* Each word is equal to the previous word, but with exactly one letter changed to a different letter of the alphabet

For example, you can go from RAM to RAT, because only one of the letters is changed (M is changed to T), and the rest of the letters stay the same.

The order of letters matters. You *cannot* rearrange letters in a word.

For example, you cannot go directly from RAM to ARM, because that would require changing two letters at once (R into A, and A into R). Instead, you would have to go through intermediate words. In this example, the shortest path is `['RAM', 'RIM', 'AIM', 'ARM']`.

In `uninformed_search.py`, you can find an empty function `find_path(start_word, end_word, word_list)`. Implement this method so that it returns the shortest path from `start_word` to `end_word`, as a list of strings.

* All words in the sequence will be the same length
* If no sequence is possible, you must return `None`
* It is assumed that both `start_word` and `end_word` are elements of `word_list`

The testing code `test.py` contains 14 different test cases. (If a test case is failed, the tester will stop, but there are 14 test cases total.)

How to run the tester, in a terminal:
```
python3 test.py
```

If a test is taking a very long time to run, that means your code is running too slowly / inefficently. (Or in some cases, you might be stuck in an infinite loop.)

Your goal is for your solution to complete all test cases in less than 1 second per test case.

Think carefully about the branching factor of your search. Naively scanning all words in the dictionary to find next steps will be too slow.
