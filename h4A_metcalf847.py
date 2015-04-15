# CSC 333 -- Homework 4 -- Stack machine interpreter
# Time-stamp: <2014-10-21 21:04:52 shade>
# Author/s: Dr. Eric Shade
#		    Zach Metcalf

# Your job is to complete the 'runvm' function. Don't change any of
# the other code. I will test your program using the 'run' function,
# which calls 'runvm' to do the heavy lifting.
#
# This code simulates a simple stack VM (virtual machine). Programs
# are written in a compact string form that is then compiled into a
# list of VM instructions. The tokens are integer literals, string
# literals in backquotes (not single quotes), names that contain one
# or more lowercase letters, and opcodes that are either single
# uppercase letters or single punctuation characters.
#
# The VM comprises a list of instructions, each of the form (opcode,
# arg); a runtime stack of integers; a list of inputs; a list of
# outputs; and a dictionary that maps variable names to their integer
# values. The default value for a variable is zero, but that can be
# changed with an S (store) instruction. The result from running the
# VM is a string containing the list of outputs joined together.
#
# See the doctests in the 'run' function for examples. The 'run'
# function calls the 'compile' function automatically, but you can use
# the 'compile' function by itself to see how programs are converted
# to lists of VM instructions.
#
# Below is a list of all the instructions. The first column shows how
# you write them in a program. The second column shows how they're
# represented in the VM after being compiled. The third column
# explains their effects.
#
# Program  VM insn       Effect (stack grows to the right)
# -------  ------------  ---------------------------------
# 417      ('#', 417)    push the integer on the stack
# `:-)`    ('`', ':-)')  write the string to the output
#
# +        ('+', None)   [___, x, y] --> [___, x+y]
# -        ('-', None)   [___, x, y] --> [___, x-y]
# *        ('*', None)   [___, x, y] --> [___, x*y]
# /        ('/', None)   [___, x, y] --> [___, x//y]
# %        ('%', None)   [___, x, y] --> [___, x%y]
# &        ('&', None)   [___, x, y] --> [___, x&y]        # bitwise and
# |        ('|', None)   [___, x, y] --> [___, x|y]        # bitwise or
# ^        ('^', None)   [___, x, y] --> [___, x^y]        # bitwise xor
# ~        ('~', None)   [___, x] --> [___, ~x]            # bitwise not
# @        ('@', None)   [___, x] --> [___, abs(x)]
# !        ('!', None)   [___, x] --> [___, int(x == 0)]
# D        ('D', None)   [___, x] --> [___, x - 1]         # [D]ecrement
# I        ('I', None)   [___, x] --> [___, x + 1]         # [I]ncrement
#
# C        ('C', None)   [___, x] --> [___, x, x]          # [C]opy
# X        ('X', None)   [___, x, y] --> [___, y, x]       # e[X]change
# Z        ('Z', None)   [___, x] --> [___]                # [Z]ap
#
# : name   ---           defines label name (maps to index of next insn)
# J name   ('J', index)  [J]ump to instruction at index
# E name   ('E', index)  pop stack; jump to index if [E]qual to zero
# G name   ('G', index)  pop stack; jump to index if [G]reater than zero
# L name   ('L', index)  pop stack; jump to index if [L]ess than zero
# N name   ('N', index)  pop stack; jump to index if [N]ot equal to zero
#
# P name   ('P', name)   [P]ush variable on stack (or zero if not defined)
# S name   ('S', name)   pop stack, [S]tore into var (create if doesn't exist)
#
# A        ('A', None)   pop stack; write chr with that [A]SCII code to output
# R        ('R', None)   [R]ead next number from input list; push on stack
# W        ('W', None)   pop stack; [W]rite number (as string) to output


import re


lexer_rules = [
    # These regexes are tried in order, from first to last, and the
    # first matching regex is used. If two different regexes might match
    # the same text, put the preferred regex first (usually the one matching
    # the longest token). The function for a regex takes the string s
    # that matched the regex and returns the corresponding token. If the
    # result is None, the lexer ignores it and finds the next token.
    (re.compile(r'\s+'),               lambda s: None),
    (re.compile(r'[ACDEGIJLNPRSWXZ]'), lambda s: s),
    (re.compile(r'[a-z]+'),            lambda s: s),
    (re.compile(r'[0-9]+'),            lambda s: int(s)),
    (re.compile(r'[-+*/%&|^~:!@]'),    lambda s: s),
    (re.compile(r'`[^`]*`'),           lambda s: s),
    (re.compile(r'.'),                 lambda s: '#?' + str(ord(s))),
]


def make_lexer(text, pos=0):
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


class CompileError(Exception):
    def __init__(self, message):
        self.message = message


def check_name(opcode, token):
    " Ensure that this token, following opcode, is a name. "

    if token is None or not token.islower():
        raise CompileError(opcode + ' must be followed by a name')
    return token


def compile(program):
    """
    Convert the program into a list of VM instructions. For
    uniformity, every VM instruction is a pair containing a
    one-character opcode and an argument; see the table above. The
    compiler detects undefined labels and duplicate labels. Labels
    don't appear as VM instructions, and jump targets are converted
    from labels to the index of the corresponding instruction in the
    VM list.
    """

    vm = []
    labels = {}
    lexer = make_lexer(program)

    token = next(lexer)
    while token is not None:
        if isinstance(token, int):
            vm.append(('#', token))
        elif token == ':':
            name = check_name(':', next(lexer))
            if name in labels:
                raise CompileError('duplicate label ' + name)
            else:
                labels[name] = len(vm)
        elif token in 'EGJLN':
            opcode = token
            name = check_name(opcode, next(lexer))
            vm.append((opcode, labels.get(name, name)))
        elif token in 'PS':
            opcode = token
            name = check_name(opcode, next(lexer))
            vm.append((opcode, name))
        elif token[0] == '`':
            vm.append(('`', token[1:-1]))
        elif token.islower():
            raise CompileError('name ' + token + ' has no preceding opcode')
        elif len(token) == 1:
            vm.append((token, None))
        else:
            raise CompileError('unrecognized opcode ' + token)
        token = next(lexer)

    # backpatch: fill in addresses for forward jumps
    for i in range(len(vm)):
        opcode, arg = vm[i]
        if opcode in 'EGJLN' and isinstance(arg, str):
            if arg in labels:
                vm[i] = (opcode, labels[arg])
            else:
                raise CompileError('undefined label ' + arg)

    return vm


def runvm(vm, rinputs):
    """
    Runs the vm, starting at instruction 0, using rinputs as the
    reversed list of inputs. In other words, the last input in the
    list is the first to be read, so you can use rinputs.pop(), a
    constant-time operation, to get the next input for an R opcode.

    """

    stack = []          # runtime stack of integers; grows to the right
    output = []         # strings that will be joined to form output
    vars = {}           # dictionary mapping varnames to integer values
    ip = 0              # instruction pointer: index of next VM insn

    while 0 <= ip < len(vm):
        opcode, arg = vm[ip]

        if opcode == '#':
            stack.append(arg)
        elif opcode == '`':
            output.append(arg)
        elif opcode == '+':
            y = stack.pop()
            x = stack.pop()
            stack.append(x + y)
        elif opcode == '-':
            y = stack.pop()
            x = stack.pop()
            stack.append(x - y)
        elif opcode == '*':
            y = stack.pop()
            x = stack.pop()
            stack.append(x * y)
        elif opcode == '/':
            y = stack.pop()
            x = stack.pop()
            stack.append(x // y)
        elif opcode == '%':
            y = stack.pop()
            x = stack.pop()
            stack.append(x % y)
        elif opcode == '&':
            y = stack.pop()
            x = stack.pop()
            stack.append(x & y)
        elif opcode == '|':
            y = stack.pop()
            x = stack.pop()
            stack.append(x | y)
        elif opcode == '^':
            y = stack.pop()
            x = stack.pop()
            stack.append(x ^ y)
        elif opcode == '~':
            x = stack.pop()
            stack.append(~x)
        elif opcode == '@':
            x = stack.pop()
            stack.append(abs(x))
        elif opcode == '!':
            x = stack.pop()
            stack.append(int(x == 0))
        elif opcode == 'D':
            x = stack.pop()
            stack.append(x - 1)
        elif opcode == 'I':
            x = stack.pop()
            stack.append(x + 1)
        elif opcode == 'C':
            x = stack.pop()
            stack.append(x)
            stack.append(x)
        elif opcode == 'X':
            x = stack.pop()
            y = stack.pop()
            stack.append(y)
            stack.append(x)
        elif opcode == 'Z':
            x = stack.pop()
        elif opcode == 'J':
            ip = arg - 1        # ip is incremented at the bottom of the loop
        elif opcode == 'E':
            num = stack.pop()
            if num == 0:
                ip = arg - 1
        elif opcode == 'G':
            num = stack.pop()
            if num > 0:
                ip = arg - 1
        elif opcode == 'L':
            num = stack.pop()
            if num < 0:
                ip = arg - 1
        elif opcode == 'N':
            num = stack.pop()
            if num != 0:
                ip = arg - 1
        elif opcode == 'P':
            if arg not in vars:
                stack.append(0)
            else:
                stack.append(vars[arg])
        elif opcode == 'S':
            num = stack.pop()
            vars[arg] = num
        elif opcode == 'A':
            code = stack.pop()
            output.append(chr(abs(code)))
        elif opcode == 'R':
            stack.append(rinputs.pop())
        elif opcode == 'W':
            num = stack.pop()
            output.append(str(num))
        else:
            raise Exception('unknown opcode ' + opcode)
        ip += 1

    return ''.join(output)


def run(program, inputs=None):
    """
    Compiles the program into a list of VM instructions, reverses the
    list of inputs (so that they can be efficiently .pop()'ed when
    [R]ead), then runs the VM. The result is the output string.

    >>> run('`2 + 2 is `2C+W33A')
    '2 + 2 is 4!'
    >>> run('2 3 + 4 *')
    ''
    >>> run('2 3 + 4 * W')
    '20'
    >>> run('9:aCLqC97+ADJa:q')
    'jihgfedcba'
    >>> run('42 Syoucanthardcodevarnames 0 Pyoucanthardcodevarnames - W')
    '-42'
    >>> run('417')
    ''
    >>> run('417W')
    '417'
    >>> run('5Jnext:nextW')
    '5'
    >>> run('`yep`')
    'yep'
    >>> run('79 76C69 72AAAAA')
    'HELLO'
    >>> run('3Na:d`:-)`Je:aJb:c4Gd:eJf:bJc:f')
    ':-)'
    >>> run('128 5 % 100 * 40 / 10 - W')
    '-3'
    >>> run('24 13 | 41 ^ 30 ~ & W')
    '32'
    >>> run('25:aCLqC65+ADJa:q')
    'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    >>> run('0RSn:tPn2%48+Pn2/CSnEgJt:gACExJg:x', [2000654321])
    '1110111001111111000111111110001'
    >>> [run('32RC65-LpC90-Ga+Jp:aC97-LpC122-GpX-:pA', [ord(c)]) for c in '@AJZ[`amz{]']
    ['@', 'a', 'j', 'z', '[', '`', 'A', 'M', 'Z', '{', ']']

    >>> [run('RC!W`,`@W', [n - 4]) for n in range(9)]
    ['0,4', '0,3', '0,2', '0,1', '1,0', '0,1', '0,2', '0,3', '0,4']

    >>> [run('RCEb0CISbSa:aDCEbPbCPa+SbSaJa:bPbW', [n]) for n in range(13)]
    ['0', '1', '1', '2', '3', '5', '8', '13', '21', '34', '55', '89', '144']

    >>> [run('0RSn:tPn2%48+Pn2/CSnEgJt:gACExJg:x', [n]) for n in range(11)]
    ['0', '1', '10', '11', '100', '101', '110', '111', '1000', '1001', '1010']

    >>> [run('RCW`+`CW`=`C+W', [n]) for n in range(2, 9)]
    ['2+2=4', '3+3=6', '4+4=8', '5+5=10', '6+6=12', '7+7=14', '8+8=16']

    >>> run('128 5 % 100 * 40 / 10 - W')
    '-3'

    >>> run('24 13 | 41 ^ 30 ~ & W')
    '32'

    >>> run('25:aCLqC65+ADJa:q')
    'ZYXWVUTSRQPONMLKJIHGFEDCBA'

    run('1 RCSaW `^` RCW ` = ` :loop CEendDXPa*X Jloop :end ZW', [3, 4])
    '3^4 = 81'

    >>> run('1 RCSaW `^` RCW ` = ` :loop CEendDXPa*X Jloop :end ZW', [123, 0])
    '123^0 = 1'

    run('1 RCSaW `^` RCW ` = ` :loop CEendDXPa*X Jloop :end ZW', [2, 31])
    '2^31 = 2147483648'

    >>> [run('RCEb0CISbSa:aDCEbPbCPa+SbSaJa:bPbW', [n]) for n in range(13)]
    ['0', '1', '1', '2', '3', '5', '8', '13', '21', '34', '55', '89', '144']

    >>> [run('0RSn:tPn2%48+Pn2/CSnEgJt:gACExJg:x', [n]) for n in range(11)]
    ['0', '1', '10', '11', '100', '101', '110', '111', '1000', '1001', '1010']

    >>> run('0RSn:tPn2%48+Pn2/CSnEgJt:gACExJg:x', [2000654321])
    '1110111001111111000111111110001'

    >>> [run('32RC65-LpC90-Ga+Jp:aC97-LpC122-GpX-:pA', [ord(c)]) for c in '@AJZ[`amz{]']    
    ['@', 'a', 'j', 'z', '[', '`', 'A', 'M', 'Z', '{', ']']

    
    """

    rinputs = [] if inputs is None else list(reversed(inputs))
    try:
        output = runvm(compile(program), rinputs)
    except CompileError as e:
        print('Error:', e.message)
        return ''
    return output


if __name__ == '__main__':
    import doctest
    doctest.testmod()
