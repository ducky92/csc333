# CSC 333 -- Recursive-descent proposition classifier
# Time-stamp: <2015-02-19 12:27:42 shade>
# Author/s: Dr. Eric Shade
#		    Zach Metcalf

import re

lexer_rules = [
    # These regexes are tried in order, from first to last, and the
    # first matching regex is used. If two different regexes might match
    # the same text, put the preferred regex first (usually the one matching
    # the longest token). The function for a regex takes the string s
    # that matched the regex and returns the corresponding token. If the
    # result is None, the lexer ignores it and finds the next token.
    (re.compile(r'\s+'),              lambda s: None),
    (re.compile(r'[FT]'),             lambda s: s == 'T'),
    (re.compile(r'[a-z]+'),           lambda s: s),
    (re.compile(r'=='),               lambda s: s),
    (re.compile(r'->|<-'),            lambda s: s),
    (re.compile(r'\\/|[&~()]'),       lambda s: s),
    (re.compile(r'.'),                lambda s: '#?' + str(ord(s))),
]

def lexer(text, pos=0):
    """
    Generates a sequence of tokens from the given string starting at
    the given position, using lexer_rules, and yielding None to
    indicate the end of the string.
    """
    while pos < len(text):
        for rule in lexer_rules:
            regex, make_token = rule
            match = regex.match(text, pos)
            if match:
                pos = match.end()
                token = make_token(match.group())
                if token is not None:
                    yield token
                    break
    yield None

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

class Parser:
    def __init__(self, text):
        self.lexer = lexer(text)
        # get the first token in preparation for parsing
        self.next()

    def error(self, message):
        raise ParseError(message + ' [next token: ' + str(self.token) + ']')

    def next(self):
        self.token = next(self.lexer)

    def parse(self):
        " input ::= eq_expr END "

        ast = self.parse_eq()
        if self.token is None:
            return ast
        else:
            self.error('extraneous input')

    def parse_eq(self):
        " eq_expr ::= imp_expr {== imp_expr}"

        ast = self.parse_imp()
        while self.token == r'==':
            self.next()
            ast = ('eq', ast, self.parse_imp())
        return ast

    def parse_imp(self):
        " imp_expr ::= revImp_expr [-> imp_expr]"

        ast = self.parse_revImp()
        if self.token == r'->':
            self.next()
            ast = ('imp', ast, self.parse_imp())
        return ast

    def parse_revImp(self):
        " revImp_expr ::= or_expr {<- or_expr}"

        ast = self.parse_or()
        while self.token == r'<-':
            self.next()
            ast = ('revImp', ast, self.parse_or())
        return ast

    def parse_or(self):
        " or_expr ::= not_expr {\/ not_expr} "

        ast = self.parse_and()
        while self.token == r'\/':
            self.next()
            ast = ('or', ast, self.parse_and())
        return ast

    def parse_and(self):
        " and_expr ::= or_expr {& or_expr}"

        ast = self.parse_not()
        while self.token == '&':
            self.next()
            ast = ('and', ast, self.parse_not())
        return ast

    def parse_not(self):
        " not_expr ::= ~ not_expr | atom "

        if self.token == '~':
            self.next()
            return ('not', self.parse_not())
        else:
            return self.parse_atom()

    def parse_atom(self):
        " atom ::= False | True | variable | '(' or_expr ')' "

        if isinstance(self.token, bool):
            ast = self.token
        elif self.token.isalpha():
            ast = self.token
        elif self.token == '(':
            self.next()
            ast = self.parse_eq()
            if self.token != ')':
                self.error("missing ')'")
        else:
            self.error("expected F, T, variable, or '('")
        self.next()
        return ast
    
def truth(variable, state):
    """
    The state is an integer whose bits encode the truth values of
    variables. For example, the state 0b1010 means that variable 0 is
    false, variable 1 is true, variable 2 is false, and variable 3 is
    true. Returns a bool indicating the truth value of this variable
    in this state.

    >>> truth(0, 0b10010)
    False
    >>> truth(2, 0b100110)
    True
    """
    return ((1 << variable) & state) != 0

eval_op = {
    'eq':  lambda s, p, q: eval(p, s) == eval(q, s),
    'imp':  lambda s, p, q: not eval(p, s) or eval(q, s),
    'revImp':  lambda s, p, q: eval(p, s) or not eval(q, s),
    'or':  lambda s, p, q: eval(p, s) or eval(q, s),
    'and': lambda s, p, q: eval(p, s) and eval(q, s),
    'not': lambda s, p: not eval(p, s),
}

def eval(p, s=0):
    """
    The value of proposition p (represented by an AST with numbered
    variables) in the state s.
    """

    if isinstance(p, bool):
        return p
    elif isinstance(p, int):
        return truth(p, s)
    else:
        operator = p[0]
        operands = p[1:]
        return eval_op[operator](s, *operands)

def variables(ast):
    """
    A sorted list of the distinct variables that appear anywhere in ast.

    >>> variables(True)
    []
    >>> variables('foo')
    ['foo']
    >>> variables(('or', ('or', 'y', ('not', 'x')), 'y'))
    ['x', 'y']
    """

    def var_set(ast):
        if isinstance(ast, str):
            return set([ast])
        elif isinstance(ast, tuple):
            return set().union(*(map(variables, ast[1:])))
        else:
            return set()

    return sorted(var_set(ast))

def number_vars(ast, vars):
    """
    Return a new ast in which all the variables are replaced by
    numbers based on their position in vars.

    >>> number_vars('p', ['apple', 'bear', 'p', 'zebra'])
    2
    >>> number_vars(('or', ('not', 'q'), 'p'), ['p','q'])
    ('or', ('not', 1), 0)
    """

    if isinstance(ast, str):
        return vars.index(ast)
    elif isinstance(ast, tuple):
        return (ast[0],) + tuple(number_vars(e, vars) for e in ast[1:])
    else:
        return ast

def classify(text):
    """
    Parses text to produce an AST, then finds the variables and
    numbers them to get a proposition p. Returns 'valid' if p is true
    in every possible state; 'satisfiable' if p is true in some but
    not all states; and 'unsatisfiable' if p is true in no states.

    >>> classify('F')
    'unsatisfiable'
    >>> classify(r'less \/ more')
    'satisfiable'
    >>> classify(r'raining \/ ~raining')
    'valid'
    >>> classify(r'p \/ p')
    'satisfiable'
    >>> classify('~(p \/ q) -> ~p & ~q')
    'valid'
    >>> classify('p -> q == q -> p')
    'satisfiable'
    >>> classify('(p -> q) -> ~q -> ~p')
    'valid'
    >>> classify('(p -> q) -> q -> p')
    'satisfiable'
    >>> classify('F  \\/  T  &  F  ->  T  ==  T')
    'valid'
    >>> classify('(snow -> skiing) & skiing -> snow')
    'satisfiable'
    >>> classify('F <- T <- F')
    'valid'
    >>> classify('x == ~y == ~(x == y)')
    'valid'
    >>> classify('(p \\/ q) & ~ p -> q')
    'valid'
    >>> classify('~(gnu == elk) == ~gnu & elk \\/ gnu & ~elk')
    'valid'
    >>> classify('p \\/ (q == r) == p \\/ q == p \\/ r')
    'valid'
    >>> classify('p == q == (p -> q) & (q -> p)')
    'valid'
    >>> classify('(alpha -> beta) -> (beta -> gamma) -> alpha -> gamma')
    'valid'
    >>> classify('foo & ~ F \\/ ~ (T -> foo)')
    'valid'
    >>> classify('(red -> blue) -> blue -> red')
    'satisfiable'
    >>> classify('(red -> blue) -> red -> blue')
    'valid'
    >>> classify('orange -> ~purple \\/ orange')
    'valid'
    >>> classify('~ (((((((((((((((orange -> purple -> orange)))))))))))))))')
    'unsatisfiable'


    """

    # COMMENT OUT ALL THE DEBUGGING PRINT STATEMENTS WHEN IT'S WORKING!

    ast = Parser(text).parse()
    #print('AST:', ast)
    vars = variables(ast)
    #print('VARS:', vars)
    p = number_vars(ast, vars)
    #print('PROP:', p)

    # TODO: check all 2**len(vars) states
    # return 'satisfiable', 'unsatisfiable', or 'valid' as necessary
    lst = list()
    for i in range(2**len(vars)):
        lst.append(eval(p, i))
    
    if lst.count(True) == (2**len(vars)):
        return 'valid'
    elif lst.count(False) == (2**len(vars)):
        return 'unsatisfiable'
    else:
        return 'satisfiable'
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    while True:
        try:
            line = input('prop> ')
        except EOFError:
            break

        if line == '' or line.isspace(): break

        try:
            print('\t', classify(line), sep='')
        except ParseError as error:
            print('parse error:', error.message)
