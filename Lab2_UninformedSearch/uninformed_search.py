from collections import deque

def find_path(start_word, end_word, word_list):
    word_list = set(word.upper() for word in word_list if len(word) == len(start_word))

    if end_word not in word_list:
        return None 
    
    queue = deque([[start_word]])
    visited = set([start_word])

    while queue: #i.e. while there are words in the queue bc if not, it means??
        path = queue.popleft()
        current_word = path[-1]

        if current_word == end_word:
            return path
    
        for i in range(len(current_word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != current_word[i]:
                    next_word = current_word[:i] + c + current_word[i+1:]
                    if next_word in word_list and next_word not in visited:
                        visited.add(next_word)
                        queue.append(path + [next_word])
    
    return None


#Plan
#breadth first search 
    #generate list of words that are found in word_list that differ by one letter only 
        #to do this, loop for each letter in word, and then swapping it for each letter of the alphabet and checking whether a) it's in word_set and b) it hasn't been visited
        #use deque from collections bc it has O(1) for popping from front 



#Same idea as w maze robot where we have a list of words and then can backtrack through them 

#for three worder

###############################See if you can change vowels first?
    #RAM > RAT (don't need to change)
    #AIM > BOT - aom /=
        #remove vowel from start check if b will work, else go through alphabet and stop when u come to smth? i.e. aim > dim
#last letter 
    #RAM > RAT: check if last letter can be changed directly to t > yes > return
    #DIM>BOT: check vowel again =/dom
        #DIM>BOT: check last letter /=dit
            #go back to changing first letter along alphabet from d onwards (and remove current_word from list)

#############################for bigger word
#lowkey same process potentially
    # figure out where vowels are supposed to go, then swap letters around to get vowels in correct space



#Popular graph algorithms like Dijkstra's shortest path, Kahn's Algorithm, and Prim's algorithm are based on BFS.  
#BFS itself can be used to detect cycle in a directed and undirected graph, find shortest path in an unweighted graph and many more problems.