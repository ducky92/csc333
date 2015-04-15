# CSC 333 DFA matcher

char_codes = {'a':1, 'b':2}

transition = [      # for b(a|bb)*b
    [0, 0, 0],      # state 0
    [0, 0, 2],      # state 1 (initial state)
    [0, 2, 3],      # state 2
    [0, 0, 2]       # state 3
]

accepting_states = {3}


def accept(s, state = 1):
    for c in s:
        state = transition[state][char_codes.get(c, 0)]
    return state in accepting_states


def trace_accept(s, state = 1):
    "same as accept, but prints a trace of the DFA"
    for c in s:
        code = char_codes.get(c, 0)
        print('\tstate ', state, ": read '", c, "' (code ", code, '): ',
              state, '---', c, '-->', sep='', end='')
        state = transition[state][code]
        print(state)
    print('\tstate ', state, ': end-of-string', sep='')
    return state in accepting_states


if __name__ == '__main__':
    while True:
        try:
            s = input('--> ')
        except EOFError:
            break

        # use accept or trace_accept
        print('\taccept' if trace_accept(s) else '\treject')
