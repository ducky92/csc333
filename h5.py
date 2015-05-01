# Author/s: Zach Metcalf
def size(ds):
    """
    Returns the total size of a data structure ds
    >>> size(['x', 4, 'y', ['a', 8, 'b', ['j', 8]]])
    20
    >>> size(['x', 4, 'y', 8, 'z', 1])
    13
    >>> size(['a', 1, 'b', ['a', 4, 'b', ['a', 1, 'b', ['a', 4, 'b', 1\
    ], 'c', 7]], 'c', 7])
    25
    >>> size((123, 4))
    492
    >>> size((10, (123, 4)))
    4920
    >>> size((10, (5, ['x', 4, 'foo', (50, 8)])))
    20200
    >>> size((1000, ['vertexCount', 4, 'vertex', (50, ['x', 4, 'y', 4])]))
    404000
    """
    total = 0
    if not isinstance(ds, tuple):
        for i in range(len(ds)):
            if isinstance(ds[i], tuple):
                total += size(ds[i])
            if isinstance(ds[i], list):
                total += size(ds[i])
            elif isinstance(ds[i],int):
                total += ds[i]
    else:
        if isinstance(ds[1], int):
            total += ds[0] * ds[1]
        elif isinstance(ds[1], tuple):
            total += ds[0] * size(ds[1])
        elif isinstance(ds[1], list):
            total += ds[0] * size(ds[1])
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
    total = 0
    
    for i in range(len(f2)):
        if f2[i] == []:
            return 0
        else:
            if isinstance(f2[i], int):
                if isinstance(f1,tuple):
                    if f2[i] <= f1[0]:
                        if isinstance(f1[1], int):
                            total += f2[i] * f1[1]
                        elif isinstance(f1[1], tuple):
                            total += f2[i] * size(f1[1])
                        elif isinstance(f1[1], list):
                            total += f2[i] * size(f1[1])
                    else:
                        total -= 1
                    f1 = f1[1]
                elif isinstance(f1, int):
                    if f2[i] == f1:
                        return 0
                    else:
                        return -1
                else:
                    if isinstance(f1, tuple):
                        if f2[i] <= f1[0]:
                            total += f1[1] * f2[i]
                        else:
                            total -= 1   
                    else:
                        return -1
            elif f2[i] not in f1:
                return -1
            else:
                a = f1.index(f2[i])
                total += size(f1[:a])
                f1 = f1[a+1]
    return total    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
