M = [ {'a':{1,2}},            # state 0
      {'b':{0}},              # state 1
      {'':{3}, 'a':{2}},      # state 2
      {'':{1}, 'b':{1}} ]     # state 3
A = {2, 3}

def nfa_eclosure (M, s):
    """
    Returns the ε-closure of state s in the NFA M, which is the
    set of all states reachable from s by zero or more ε-edges.
    Note that the ε-closure of s always includes s itself. Also
    note that the NFA might contain ε-cycles.

    >>> nfa_eclosure(M, 0)
    {0}
    >>> nfa_eclosure(M, 2)
    {1, 2, 3}
    >>> nfa_eclosure([{'':{1}}, {'':{2}}, {'':{3}}, {'':{4}}, {'':{0}}], 0)
    {0, 1, 2, 3, 4}
    """
    eclosure = {s}
    for i in range(len(M)):
        for j in range(len(M)):
            if j in eclosure:
                if '' in M[j]:
                    eclosure = eclosure.union(M[j][''])

    return eclosure

def nfa_accepts(M, A, x):
    """
    Takes an NFA M, a set A of accepting states, and a string x.
    Returns True if M accepts x and False otherwise. The string
    x can contain any characters, including ones not mentioned
    in the NFA, and it can be empty.

    >>> nfa_accepts(M, A, '')
    False
    >>> nfa_accepts(M, A, 'aabb')
    False
    >>> nfa_accepts(M, A, 'aabba')
    True
    >>> [nfa_accepts([{'':{1},'a':{2}},{'':{2}},{'b':{1,3}},{'a':{1,3}}], {1,3}, x) for x in ['','a','b','babba','aaba','baaabbaaaabbbaaaaa','baaabbaaaabXbbaaaaa']]
    [True, False, True, True, False, True, False]
    >>> [nfa_accepts([{}], {0}, x) for x in ['','a',100*'a']]
    [True, False, False]
    >>> [nfa_accepts([{'':{1},'s':{1}},{'d':{1,2}},{'':{4},'.':{3}},{'d':{3,4}},{'':{7},'e':{5}},{'':{6},'s':{6}},{'d':{7}},{'d':{7}}], {7}, x) for x in ['','.','s','e','ds','ss','dede','ddsed','dd.esdd','d',100*'d','sd','ded','desd','d.d','d.ddeddd','sddd.ddddesddd']]
    [False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True]
    >>> [nfa_accepts([{'a':{0}},{'b':{0,1}}], {0}, n*'a') for n in range(10)]
    [True, True, True, True, True, True, True, True, True, True]
    """
    states = {0}
    
    lst = []
    for i in range(len(M)):
        lst.append(nfa_eclosure(M, i))

    #if x == '' and 0 in A:
    #    return True


    for c in x:
        next_set = set()
        for i in states: # add acceptable states to set
            states = states.union(lst[i])
        
        for i in states:
            for k in M[i]: # if c is a key of current state
                if c == k:
                    for j in M[i][k]:
                        next_set.add(j)
        states = next_set
    

        
    final = set()
    for i in states:
        final = final.union(lst[i])
        #final = final.union(s)
    
    for i in final:
        if i in A:
            return True

    return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
