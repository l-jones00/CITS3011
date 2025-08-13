##informed search using heuristic Hamming Distance
# this uses a PRIORITY QUEUE

import heapq
#use a min-heap where lower f(n) values come out first

def hamming_distance(word1, word2):
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))

    #1. zip(word1, word2) → gives pairs like ('M', 'B'), ('A', 'A'), etc.
    #2. c1 != c2 → checks whether each pair of letters is different (True/False)
    #3. sum(...) → counts how many True values (differences) there are.

def find_path_a_star(start_word, end_word, word_list):
    word_list = set(word.upper() for word in word_list if len(word) == len(start_word))

    if end_word not in word_list:
        return None
    
    heap = []
    heapq.heappush(heap, (hamming_distance(start_word, end_word), [start_word]))
    visited = set()

    while heap:
        f_cost, path = heapq.heappop(heap)
        current_word = path[-1]

        if current_word == end_word:
            return path
        
        if current_word in visited:
            continue
        visited.add(current_word)

        for i in range(len(current_word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != current_word[i]:
                    next_word = current_word[:i] + c + current_word[i+1:]
                    if next_word in word_list and next_word not in visited:
                        g_cost = len(path)  # steps so far
                        h_cost = hamming_distance(next_word, end_word)
                        f_cost = g_cost + h_cost
                        heapq.heappush(heap, (f_cost, path + [next_word]))

        
    return None
