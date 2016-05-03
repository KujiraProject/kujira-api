""" Example docstring """


def square(arg):
    """
    Example function
    @param arg: Arg 1
    """
    return arg**2


def test_square():
    """ Test square function """
    arg = 4
    assert square(arg) == 16


def square2(arg):
    """Return the square of a number `argx`.

    [...]

    Examples
    --------
    >>> square(5)
    25
    """
    return arg ** 2
