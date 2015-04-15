
def size(ds):
    """
    Returns the total size of a data structure ds
    >>> size(['x', 4, 'y', ['a', 8, 'b', ['j', 8]]])
    20
    >>> size(['x', 4, 'y', 8, 'z', 1])
    13
    >>> size(['a', 1, 'b', ['a', 4, 'b', ['a', 1, 'b', ['a', 4, 'b', 1], 'c', 7]], 'c', 7])
    25
    """
    total = 0
    for i in range(len(ds)):
        if isinstance(ds[i], str) and isinstance(ds[i+1], int):
            total += ds[i + 1]
        elif isinstance(ds[i], str) and isinstance(ds[i + 1], list):
            total += size(ds[i+1])
    return total

def offset(f1, f2):
    """
    >>> offset(8, [])
    0
    >>> offset(4, [1])
    -1
    >>> offset(['x', 4, 'y', 8, 'z', 1], ['z'])
    12
    >>> offset(['x', 4, 'y', 8, 'z', 1], ['foo'])
    -1
    >>> offset(['x', 4, 'y', 8, 'z', 1], [24, 'q', 4, 'foo'])
    -1
    >>> offset(['a', 1, 'b', ['a', 4, 'b', 1], 'c', 7], ['b'])
    1
    >>> offset(['a', 1, 'b', ['a', 4, 'b', 1], 'c', 7], ['c'])
    6
    >>> offset(['a', 1, 'b', ['a', 4, 'b', 1], 'c', 7], ['b', 'b'])
    5
    >>> offset(['a', 1, 'b', ['a', 4, 'b', 1], 'c', 7], ['b', 'c'])
    -1
    >>> offset((123, 4), [10])
    40
    >>> offset((123, 4), [1000])
    -1
    >>> offset((10, (5, ['x', 4, 'foo', (50, 8)])), [2, 3, 'foo', 4])
    5288

    """

    if isinstance(f1, int) and isinstance(f2, lst): # (n, ds)
        pass
    elif isinstance(f1, list):
        pass
    


if __name__ == '__main__':
    import doctest
    doctest.testmod()
