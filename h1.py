# CSC 333 - Spring 2015 - Homework 1
# Time-stamp: <2015-01-22 12:52:03 shade>
# Author/s: Dr. Eric Shade
#           Zach Metcalf

# Complete all of the following functions. Currently they all just
# 'pass' rather than explicitly return a value, which means that they
# implicitly return None. They all include doctests, which you can
# test by running this file as a script: python h1.py

# The doctests are just examples. I will run additional tests when I
# grade your homework. Feel free to add your own doctests.

def take(n, iterable):
    """
    Return a list of the first n items in iterable. If n <= 0, return
    the empty list. Do not consume MORE than n items of iterable.

    >>> take(2, 'football')
    ['f', 'o']
    >>> take(5, range(73, 100))
    [73, 74, 75, 76, 77]
    >>> take(-5, range(73, 100))
    []
    """
    
    lst = []
    ctr = 0 
    if n <=0:
        return []
    iterable = iter(iterable)
    while ctr != n:
        lst.append(next(iterable))
        ctr +=1    
    
    return lst

def clamp(f, lo, hi):
    """
    Return a function like f except that the result is clamped to the
    range lo..hi, where you can assume that lo <= hi. Given x, the new
    function should return f(x) if lo <= f(x) <= hi, or else return lo
    or hi depending on whether f(x) is below or above the range.
    The new function must only evaluate f once each time it's called.

    >>> clamp(lambda x: 2*x - 5, 0, 10)(6)
    7
    >>> clamp(lambda x: 2*x - 5, 0, 10)(1)
    0
    """
    #pass
    def inside(x):
        result = f(x)
        if(result > hi):
           return hi
        elif (result < lo):
           return lo
        else:
           return result
    return lambda x: inside(x)

def genfib(a, b, f):
    """
    The standard Fibonacci sequence looks like this:

        fib(0) = 0
        fib(1) = 1
        fib(n) = fib(n-2) + fib(n-1), for n > 1

    genfib must generate (using yield) the generalized Fibonacci
    sequence, where the first two elements are a and b, and successive
    elements are obtained by applying f to the previous two elements,
    rather than adding them. Note that the first argument to f is the
    earlier of the two previous elements.

    >>> take(5, genfib(0, 1, lambda x, y: x - y))
    [0, 1, -1, 2, -3]
    >>> take(6, genfib(1, -2, lambda x, y: x * y))
    [1, -2, -2, 4, -8, -32]
    >>> take(4, genfib('', 'a', lambda x, y: x + y))
    ['', 'a', 'a', 'aa']

    """
    #pass
    yield a
    yield b
    while True:
        result = f(a,b)
        a = b
        b = result
        yield result

def invert(d):
    """
    Return the inverse of dictionary d: a dictionary that maps the
    values of d to the keys of d. If a value in d appears more than
    once, then it must map to the SET (not the list) of all keys with
    that value in d. Note: you can assume that all the values in d are
    also valid dictionary keys. Thus they can't be sets, or any other
    non-hashable type.

    >>> sorted(invert({'a':1, 'b':2}).items())
    [(1, 'a'), (2, 'b')]
    >>> sorted(invert({'a':1, 'b':2, 'c':1}).items())
    [(1, {'a', 'c'}), (2, 'b')]
    >>> invert({1:1})
    {1: 1}
    >>> sorted(invert({n:n+1 for n in range(7)}).items())
    [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]
    >>> sorted(invert({1:2,2:2,3:3,4:3,5:6,7:3,8:2}).items())
    [(2, {8, 1, 2}), (3, {3, 4, 7}), (6, 5)]


    """
    # pass
    inv_d = {}

    for k,v in d.items():
        if not v in inv_d.keys(): # not in dict
            inv_d[v] = k
        else: # is in dict
            if type(inv_d[v]) is set:
                inv_d[v].add(k)                
            else:
                s = set()
                s.add(inv_d[v]) # add whats already there
                s.add(k)
                inv_d[v] = s                
            
    return inv_d

def find_best(f, xs):
    """
    Assume that f(x) gives a measure of the "goodness" of x, where
    larger values are better than smaller ones. Return the best element
    of the nonempty list xs. If two or more elements are equally good,
    return the one that appears earliest in the list.

    >>> find_best(lambda x: x ** 2, [4,-5,2,5,-3,0,1])
    -5
    >>> find_best(lambda s: s[1:], ['fox','moose','frog','goat'])
    'frog'
    """
    #pass
    best = xs[0]
    for x in xs:
        if f(x) > f(best):
            best = x
    return best
            

def trim(p, xs):
    """
    Removes all leading and trailing elements that satisfy predicate p
    from the list xs. You can either mutate xs or return a new list.

    >>> trim(lambda x: x%2 == 0, [8,6,7,5,2,4,3,0,9])
    [7, 5, 2, 4, 3, 0, 9]
    >>> ''.join(trim(str.isupper, list('FOrMuLAIC')))
    'rMu'

    """
    #pass
    begin, end = 0,0
    for i in range(len(xs)):
        if p(xs[i]) == False:
            begin = i
            break
    for i in range(len(xs), 0, -1):
        if p(xs[i-1]) == False:
            end = i
            break
    return xs[begin:end]

def deep_reverse(xs):
    """
    If xs is not a list, return xs. If xs is a list, return the deep
    reversal of xs, in which xs and all sublists, nested to any depth,
    are reversed. It's easiest to recursively build a new
    deep-reversed list, rather than trying to modify the original list.

    >>> isinstance('bob', list)
    False
    >>> deep_reverse('bob')
    'bob'
    >>> deep_reverse([1,2,3])
    [3, 2, 1]
    >>> deep_reverse([[[1, [2, 3], 4]], 5, [[6, 7], 8]])
    [[8, [7, 6]], 5, [[4, [3, 2], 1]]]

    """
    #pass
    reverse = []
    if isinstance(xs, list):
        for i in xs:
            if isinstance(i, list):
                reverse.append(deep_reverse(i))
            else:
                reverse.append(i)
        reverse.reverse()
        return reverse
    else:
        return xs
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
